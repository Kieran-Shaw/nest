import os

from pyairtable import Table


class WriteServiceItems:
    def __init__(self, table_id_list: list):
        self.auth_token = os.getenv("AIRTABLE_TOKEN")
        self.base_id = os.getenv("BASE_ID")
        self.table_id_list = table_id_list

    def create_records(self, table_name: str, record_list: list):
        table_id = next(
            (item["id"] for item in self.table_id_list if item["name"] == table_name),
            None,
        )

        if not table_id:
            raise ValueError(f"Table name '{table_name}' not found in table_id_dict.")

        table = Table(self.auth_token, self.base_id, table_id)

        return_objects = table.batch_create(records=record_list)

        return [item["id"] for item in return_objects]
