from modules.business_logic.get_service_template import ServiceTemplateQuerier
from datetime import datetime
import json

class ServiceCreationError(Exception):
    pass

def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

config = load_config('config.json')

class CreateServicePlan:
    def __init__(self, create_object: dict, logger):
        self.client_id = create_object["data"]["client_id"]
        self.service_create_id = create_object["data"]["record_id"]
        self.group_size = create_object["data"]["group_size"]
        self.funding_tag = create_object["data"]["funding_tag"]
        self.conditionals = create_object["data"]["conditionals"]
        self.renewal_date = datetime.strptime(create_object["data"]["renewal_date"], '%Y-%m-%d')
        self.template_table_ids = config["template"]
        self.write_table_ids = config["write"]
        self.service_template = None

        # Store the logger
        self.logger = logger

        # Log initialization
        self.logger.info(f"Initializing CreateServicePlan with client_id: {self.client_id} and service_create_id: {self.service_create_id}")
        
        # Create the service plan upon instantiation
        self._status_code = self.create_service_plan()

    def create_service_plan(self):
        # Log the service plan creation attempt
        self.logger.info(f"Attempting to create service plan for client_id: {self.client_id}")

        # Query Service Template
        self.service_template = ServiceTemplateQuerier(table_id_dict=self.template_table_ids).query_all_tables()

        # with open('response.json', 'w') as json_file:
        #     json.dump(self.service_template, json_file)

        if not self.service_template:
            # Log the failure to fetch the service template
            self.logger.error(f"Failed to query service template for client_id: {self.client_id}")
            
            # Set the status code to indicate failure and raise an error
            self._status_code = 400
            raise ServiceCreationError("Failed to query service template.")
        
        # Add logic for creating the service plan...
        applicable_tasks = self.applicable_tasks()
        applicable_milestones = self.applicable_milestones(applicable_tasks=applicable_tasks)
        applicable_buckets = self.applicable_buckets(applicable_milestones=applicable_milestones)
        
        # create objects to then write to airtable

        # Log success
        self.logger.info(f"Successfully created service plan for client_id: {self.client_id}")

        # Assuming the service plan creation is successful
        self._status_code = 200
        
        return self._status_code

    @property
    def status_code(self):
        return self._status_code
    
    def applicable_tasks(self):
        tasks = self.service_template["tasks"]
        group_size_tasks = self.group_size_filter(tasks=tasks)
        return
    
    def applicable_milestones(self,applicable_tasks:dict):
        return
    
    def applicable_buckets(self,applicable_milestones:dict):
        return
    
    def group_size_filter(self, tasks:dict):
        # target id
        target_id = self.group_size[0]
        # List to store the matched tasks
        matched_tasks = []
        # Iterating through the tasks to find matches
        for task in tasks:
            if "Group Size" in task["fields"] and self.group_size in task["fields"]["Group Size"]:
                matched_tasks.append(task)

        return matched_tasks
    
    def conditional_filter(self, group_size_tasks):
        return
        


