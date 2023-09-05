from business_logic.airtable_methods import ServiceTemplateQuerier, WriteServiceItems
import json

class ServiceCreationError(Exception):
    pass

def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

config = load_config('config/config.json')

class CreateOnboarding:
    def __init__(self, create_object: dict, logger):
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
        # keep only for onboarding



        return