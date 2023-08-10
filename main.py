from flask import Flask, jsonify, request
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

    if os.getenv('LOCATION') == 'LOCAL':
        app.config['DEBUG'] = True

    # instantiate AirtableClient
    # airtable_client = AirtableClient(logger=logger)

    @app.route('/')
    def base_request():
        app.logger.info('Base URL')
        return f'Base NEST URL, Please Specify Which Endpoint To Take An Action', 200

    @app.route('/create', methods=['POST'])
    def create_service_plan():
        app.logger.info('Starting creation of service plan...')
        data = request.json
        client_name = 'Demo Company'
        status_code = 200
        app.logger.info(f'Finished creation of service plan: INFORMATION')
        return f'Service Plan Created: {client_name}', status_code
    
    @app.route('/delete', methods=['POST'])
    def delete_service_plan():
        app.logger.info('Starting deletion of service plan...')
        data = request.json
        client_name = 'Demo Company'
        status_code = 200
        app.logger.info(f'Finished deletion of service plan: INFORMATION')
        return f'Service Plan Deleted: {client_name}', status_code
    
    @app.route('/refactor', methods=['POST'])
    def refactor_service_plan():
        app.logger.info('Starting refactor of service plan...')
        data = request.json
        client_name = 'Demo Company'
        status_code = 200
        app.logger.info(f'Finished refactor of service plans: INFORMATION')
        return f'Service Plan Refactored: {client_name}', status_code
    
    @app.route('/update', methods=['POST'])
    def update_service_plans():
        app.logger.info('Starting update of service plans...')
        data = request.json
        client_name = ['Demo Company','ACME Corp']
        status_code = 200
        app.logger.info(f'Finished update of service plans: INFORMATION')
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
