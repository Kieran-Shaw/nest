import json
import boto3

class SecretsManagerClient:
    def __init__(self, logger, local_dev: bool = True, region_name: str = "us-east-1"):
        self.logger = logger
        if local_dev:
            self.logger.info('SecretsManager Local Dev')
            session = boto3.Session(profile_name='kieran_dev')
        else:
            self.logger.info('SecretsManager Cloud Session')
            session = boto3.Session()
        # client
        self.client = session.client('secretsmanager', region_name=region_name)

    def get_secret(self, secret_name):
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            if 'SecretString' in response:
                secret = response['SecretString']
                return json.loads(secret)
        except Exception as e:
            self.logger.error(f"Error fetching secret: {e}")
            return None
