import os

from pyairtable import Table


class ServiceTemplateQuerier:
    def __init__(self, table_id_list: list):
        self.auth_token = os.getenv("AIRTABLE_TOKEN")
        self.base_id = os.getenv("BASE_ID")
        self.table_id_list = table_id_list

    def query_table(self, table_id):
        table = Table(self.auth_token, self.base_id, table_id)
        return table.all()

    def query_all_tables(self):
        results = {}
        for template_object in self.table_id_list:
            results[template_object["name"]] = self.query_table(template_object["id"])
        return results
