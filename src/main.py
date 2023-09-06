from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from methods.create_service_plan import CreateServicePlan
from methods.create_onboarding import CreateOnboarding
import logging

# Set up global logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    load_dotenv()  # Load environment variables from .env file

    if os.getenv('LOCATION') == 'LOCAL':
        app.config['DEBUG'] = True

    @app.route('/')
    def base_request():
        logger.info('Base URL')
        return f'Base NEST URL, Please Specify Which Endpoint To Take An Action', 200

    @app.route('/create', methods=['POST'])
    def create_service_plan():
        data = request.json
        logger.info(f'Starting creation of service plan for {data["client_name"]}')
        service_plan_status = CreateServicePlan(create_object=data,logger=logger).create_service_plan()
        logger.info(f'Finished creation of service plan for {data["client_name"]}')
        return f'Service Plan Created: {data["client_name"]}', service_plan_status.status_code
    
    @app.route('/delete', methods=['POST'])
    def delete_service_plan():
        logger.info('Starting deletion of service plan...')
        data = request.json
        client_name = 'Demo Company'
        status_code = 200
        logger.info(f'Finished deletion of service plan: INFORMATION')
        return f'Service Plan Deleted: {client_name}', status_code
    
    @app.route('/refactor', methods=['POST'])
    def refactor_service_plan():
        logger.info('Starting refactor of service plan...')
        data = request.json
        client_name = 'Demo Company'
        status_code = 200
        logger.info(f'Finished refactor of service plans: INFORMATION')
        return f'Service Plan Refactored: {client_name}', status_code
    
    @app.route('/update', methods=['POST'])
    def update_service_plans():
        logger.info('Starting update of service plans...')
        data = request.json
        client_name = ['Demo Company','ACME Corp']
        status_code = 200
        logger.info(f'Finished update of service plans: INFORMATION')
        return f'Service Plans Updated: {client_name}', status_code
    
    @app.route('/onboarding', methods=['POST'])
    def create_onboarding():
        logger.info('Starting creation of onboarding')
        data = request.json
        onboarding_status = CreateOnboarding(create_object=data, logger=logger)
        logger.info(f'Created onboarding for {data["client_name"]}')
        return f'Service Plans Updated: {data["client_name"]}', onboarding_status.status_code

    @app.route('/favicon.ico')
    def favicon():
        return '', 204
    
    @app.errorhandler(404)
    def page_not_found(e):
        logger.error('Page not found')
        return jsonify(error=str(e)), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        logger.error('Server error')
        return jsonify(error=str(e)), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')))
