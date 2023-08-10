from flask import Flask, jsonify
from modules.airtable_client import AirtableClient
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

    local_dev = os.getenv('LOCATION')
    if local_dev == 'LOCAL':
        app.config['DEBUG'] = True

    @app.route('/')
    def base_request():
        app.logger.info('Base URL')
        # instantiate AirtableClient
        airtable_client = AirtableClient(logger=logger)
        return f'Base NEST URL, Please Specify Which Endpoint To Take An Action', 200

    @app.route('/create')
    def create_service_plan():
        app.logger.info('Starting creation of service plan...')
        client_name = 'Demo Company'
        status_code = 200
        return f'Service Plan Created: {client_name}', status_code
    
    @app.route('/delete')
    def delete_service_plan():
        app.logger.info('Starting deletion of service plan...')
        client_name = 'Demo Company'
        status_code = 200
        return f'Service Plan Deleted: {client_name}', status_code
    
    @app.route('/refactor')
    def refactor_service_plan():
        app.logger.info('Starting refactor of service plan...')
        client_name = 'Demo Company'
        status_code = 200
        return f'Service Plan Refactored: {client_name}', status_code
    
    @app.route('/update')
    def update_service_plans():
        app.logger.info('Starting update of service plans...')
        client_name = ['Demo Company','ACME Corp']
        status_code = 200
        return f'Service Plans Updated: {client_name}', status_code

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
