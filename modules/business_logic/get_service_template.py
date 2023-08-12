from pyairtable import Table
import os

class ServiceTemplateQuerier:
    def __init__(self,table_id_dict:dict):
        self.auth_token = os.getenv('AIRTABLE_TOKEN')
        self.base_id = os.getenv('BASE_ID')
        self.table_id_dict = table_id_dict

    def query_table(self, table_id):
        table = Table(self.auth_token, self.base_id, table_id)
        return table.all()

    def query_all_tables(self):
        results = {}
        for template_object in self.table_id_dict:
            results[template_object["name"]] = self.query_table(template_object["id"])
        return results
