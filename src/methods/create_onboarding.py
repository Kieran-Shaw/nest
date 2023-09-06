from business_logic.airtable_methods import ServiceTemplateQuerier, WriteServiceItems
from methods.create_service_plan import CreateServicePlan
import json

class ServiceCreationError(Exception):
    pass

def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

config = load_config('config/config.json')

class CreateOnboarding:
    def __init__(self, create_object: dict, logger):
        self.create_object = create_object
        self.client_id = create_object["client_id"]
        self.service_create_id = create_object["service_plan_id"]
        self.client_name = create_object["client_name"]
        self.template_table_ids = config["template"]
        self.logger = logger

        # Log initialization
        self.logger.info(f"Initializing CreateOnboarding with client_id: {self.client_id} and service_create_id: {self.service_create_id}")
        
        # Create the service plan upon instantiation
        self._status_code = self.create_onboarding()

    @property
    def status_code(self):
        return self._status_code

    def create_onboarding(self):
        # get all service items
        self.service_template = ServiceTemplateQuerier(table_id_list=self.template_table_ids).query_all_tables()

        # create full service plan (we can use the code to create a service plan then filter JUST for onboarding)
        service_plan = CreateServicePlan(create_object=self.create_object,logger=self.logger).create_service_plan(onboarding=True)
        
        with open('dev/responses/onboarding.json', 'w') as f:
            json.dump(service_plan, f, indent=4)


        return
    
    def onboarding_filter(self):
        # iterate through the buckets to find only the applicable buckets

        # iterate through the milestones to find only the applicable milestones

        # iterate through the tasks to find only the applicable tasks

        return
    
    def onboarding_bucket(self):
        # find all onboarding related buckets
        onboarding_bucket_id = config["onboarding"]["id"]
