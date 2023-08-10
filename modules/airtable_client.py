from pyairtable import Table
import os

class AirtableClient:
    def __init__(self,logger):
        self.airtable_token = os.getenv('AIRTABLE_TOKEN')
        self.logger = logger

        if self.airtable_token:
            self.logger.info(f"Successfully retrieved secret for key: AIRTABLE_TOKEN")
            # Do something with the token, like initializing your connection to Airtable
            pass
        else:
            # Maybe raise an error or log that the token is missing
            self.logger.info(f"Secret not found for key: AIRTABLE_TOKEN")
            pass