from business_logic.airtable_methods import ServiceTemplateQuerier, WriteServiceItems
import json
from typing import Optional

class ServiceCreationError(Exception):
    pass

def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

config = load_config('config/config.json')

class CreateServicePlan:
    def __init__(self, create_object: dict, logger, onboarding_only: bool = False):
        self.client_id: str = create_object["client_id"]
        self.service_create_id: str = create_object["service_plan_id"]
        self.group_size: Optional[str] = None
        self.conditionals: Optional[str] = None
        self.template_table_ids: Optional[str] = None
        self.write_table_ids: Optional[str] = None
        self.service_template = None

        # Store the logger
        self.logger = logger

        if not onboarding_only:
            self.logger.info(f"Initializing Full CreateServicePlan with client_id: {self.client_id} and service_create_id: {self.service_create_id}")
            self._initialize_full(create_object=create_object)
        
        if onboarding_only:
            self.logger.info(f"Initializing Onboarding Only CreateServicePlan with client_id: {self.client_id} and service_create_id: {self.service_create_id}")
    
    def _initialize_full(self, create_object: dict):
        # Helper function to initialize attributes that are only relevant when onboarding_only is False
        self.group_size = create_object["group_size_id"]
        self.conditionals = create_object["conditionals_id"]
        self.template_table_ids = config["template"]
        self.write_table_ids = config["write"]
    
    def _initialize_onboarding(self, create_object: dict):
        # Helper function to initialize attributes that are only relevant when onboarding_only is True
        self.group_size = create_object["group_size_id"]
        self.conditionals = create_object["conditionals_id"]
        self.template_table_ids = config["template"]
        self.write_table_ids = config["write"]

    def create_service_plan(self,onboarding: bool = False):
        # Log the service plan creation attempt
        self.logger.info(f"Attempting to create service plan for client_id: {self.client_id}, Onboarding = {onboarding}")

        # Query Service Template
        self.service_template = ServiceTemplateQuerier(table_id_list=self.template_table_ids).query_all_tables()

        if not self.service_template:
            # Log the failure to fetch the service template
            self.logger.error(f"Failed to query service template for client_id: {self.client_id}")
            
            # Set the status code to indicate failure and raise an error
            self._status_code = 400
            raise ServiceCreationError("Failed to query service template.")
        
        # Add logic for creating the service plan...
        write_client = WriteServiceItems(table_id_list=self.write_table_ids)
        # Find applicable tasks, milestones, buckets & create service_plan
        applicable_tasks = self.applicable_tasks()
        grouped_by_bucket = self.group_by_bucket(milestones=self.service_template["milestones"],applicable_tasks=applicable_tasks)

        # if we are just returning the service_template
        if onboarding:
            return grouped_by_bucket
        
        create_buckets = self.write_records(write_client=write_client, grouped_by_bucket=grouped_by_bucket)

        if not create_buckets:
            self._status_code = 400
            raise ServiceCreationError("Failed to create service plan, check logs")
        
        # Log success
        self._status_code = 200
        self.logger.info(f"Successfully created service plan for client_id: {self.client_id}")
        return self._status_code

    @property
    def status_code(self):
        return self._status_code
    
    def applicable_tasks(self):
        tasks = self.service_template["tasks"]
        group_size_tasks = self.group_size_filter(tasks=tasks)
        group_size_conditional = self.conditional_filter(tasks=tasks,group_size_tasks=group_size_tasks)
        return group_size_conditional

    def group_size_filter(self, tasks: list):
        # List to store the matched tasks
        matched_tasks = []
        # Iterating through the tasks to find matches
        for task in tasks:
            if "Group Size" in task["fields"] and self.group_size in task["fields"]["Group Size"]:
                matched_tasks.append(task)
        return matched_tasks
    
    def conditional_filter(self, tasks: list, group_size_tasks: list):
        # Iterating through the group_size_tasks to find matches for conditionals
        for task in tasks:
            if "Conditionals" in task["fields"] and set(task["fields"]["Conditionals"]) & set(self.conditionals):
                group_size_tasks.append(task)
        return group_size_tasks
    
    def task_id_to_object(self,applicable_tasks:list):
        # Assuming tasks is your original list of task objects
        task_id_to_object = {task["id"]: task for task in applicable_tasks}
        return task_id_to_object

    def structure_object(self, grouped_by_bucket: dict):
        grouped_by_bucket_cleaned = {}

        for bucket_id, milestones in grouped_by_bucket.items():
            grouped_by_bucket_cleaned[bucket_id] = {}

            for milestone_id, tasks in milestones.items():
                grouped_by_bucket_cleaned[bucket_id][milestone_id] = [{"[Template] Tasks": [task["id"]]} for task in tasks]
        
        return grouped_by_bucket_cleaned
    
    def group_by_bucket(self, milestones: list, applicable_tasks: list):
        # return the lookup dictionaries
        task_id_to_object = self.task_id_to_object(applicable_tasks=applicable_tasks)

        grouped_by_bucket = {}

        # Start by grouping by [Template] Buckets
        for milestone in milestones:
            bucket = milestone["fields"]["[Template] Buckets"][0]  # Assuming there's only one bucket per milestone

            # Collect applicable tasks for this milestone
            applicable_tasks = [task_id_to_object[task_id] for task_id in milestone["fields"]["[Template] Tasks"] if task_id in task_id_to_object]
            
            # If there are no applicable tasks, we skip this milestone
            if not applicable_tasks:
                continue

            # If there are applicable tasks, then process further
            if bucket not in grouped_by_bucket:
                grouped_by_bucket[bucket] = {}

            # Add the milestone and its applicable tasks under the respective bucket
            grouped_by_bucket[bucket][milestone["id"]] = applicable_tasks

        cleaned_grouped_by_bucket = self.structure_object(grouped_by_bucket=grouped_by_bucket)

        return cleaned_grouped_by_bucket
    
    def write_records(self, write_client: WriteServiceItems, grouped_by_bucket: dict):
        bucket_data_list = []

        for bucket_id, milestones in grouped_by_bucket.items():
            milestone_data_list = []
            
            for milestone_id, tasks in milestones.items():
                created_task_ids = write_client.create_records(table_name="tasks",record_list=tasks)
                milestone_data = {
                    "[Template] Milestones": [milestone_id],
                    "Tasks": created_task_ids
                }
                milestone_data_list.append(milestone_data)

            created_milestone_ids = write_client.create_records(table_name="milestones",record_list=milestone_data_list)

            bucket_data = {
                "[Template] Buckets": [bucket_id],
                "Milestones": created_milestone_ids,
                "ServicePlans": [self.service_create_id],
                "Service Plan Dates": [self.bucket_date(bucket_id=bucket_id)]
            }
            bucket_data_list.append(bucket_data)

        created_bucket_ids = write_client.create_records(table_name="buckets",record_list=bucket_data_list)
        return created_bucket_ids
    
    def bucket_date(self, bucket_id: str):
        for object in self.service_template["dates"]:
            if bucket_id in object["fields"]["Service Journey Buckets"] and self.group_size in object["fields"]["Group Size"][0]:
                return object["id"]
        raise ValueError(f"Group Size '{self.group_size} and Bucket '{bucket_id} not found")




        


