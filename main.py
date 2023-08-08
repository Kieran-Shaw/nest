from flask import Flask, jsonify
from modules.airtable_client import AirtableClient
from modules.secrets_client import SecretsManagerClient
from dotenv import load_dotenv
import os
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)

def create_app():
    app = Flask(__name__)

    load_dotenv()  # Load environment variables from .env file
    setup_logging()  # Set up logging configuration
    logger = app.logger  # Get the Flask app's logger instance

    local_dev = os.getenv('LOCAL_DEV',False)
    if local_dev:
        app.config['DEBUG'] = True

    # Usage:
    secrets_manager_client = SecretsManagerClient(logger=logger,local_dev=local_dev)
    sample = None
    secret = secrets_manager_client.get_secret("prod/airtable_oauth")
    if secret:
        sample = 'We Found It!'

    @app.route('/')
    def base_request():
        app.logger.info('Base URL Hit')
        return f'Base NEST URL, Please Specify Which Endpoint To Take An Action: {sample}', 200

    @app.route('/service-plan-creation')
    def hello_world():
        app.logger.info('Processing service plan creation')
        return 'Hello, World!'

    @app.route('/favicon.ico')
    def favicon():
        return '', 204
    
    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.error('Page not found')
        return jsonify(error=str(e)), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error('Server error')
        return jsonify(error=str(e)), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')))
