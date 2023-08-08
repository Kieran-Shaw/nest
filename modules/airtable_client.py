from pyairtable import Table
import boto3

class AirtableClient:
    def __init__(self, secret_name, region):
        self.secret_name = secret_name
        self.client = boto3.client('secretsmanager', region_name=region)

    def get_parameters(self):
        response = self.client.get_secret_value(SecretId=self.secret_name)
        # Assuming the secret value is a string (e.g., API key)
        access_token = response['SecretString']        
        return access_token