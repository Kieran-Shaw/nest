import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from config.config import DevelopmentConfig, ProductionConfig
from service_plans.create_onboarding import CreateOnboarding
from service_plans.create_service_plan import CreateServicePlan


# configure logging
def configure_logging(app):
    log_level = app.config.get("LOG_LEVEL", logging.INFO)

    if os.getenv("ENVIRONMENT") == "aws":
        # AWS environment, let CloudWatch handle logging.
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )
    else:
        # Local or other environments, file and stream based logging.
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("logs/application.log"),
            ],
        )


# create application
def create_app():
    app = Flask(__name__)
    app.logger = logging.getLogger(__name__)

    load_dotenv()  # Load environment variables from .env file

    env = os.getenv("FLASK_ENV", "production")

    if env == "development":
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    configure_logging(app)

    @app.route("/")
    def base_request():
        app.logger.info("Base URL")
        return f"Base CRUD Operation NEST Endpoint", 200

    @app.route("/create", methods=["POST"])
    def create_service_plan():
        data = request.json
        app.logger.info(f'Starting creation of service plan for {data["client_name"]}')
        service_plan_status = CreateServicePlan(
            create_object=data, logger=app.logger
        ).create_service_plan()
        app.logger.info(f'Finished creation of service plan for {data["client_name"]}')
        return (
            f'Service Plan Created: {data["client_name"]}',
            service_plan_status.status_code,
        )

    @app.route("/delete", methods=["POST"])
    def delete_service_plan():
        app.logger.info("Starting deletion of service plan...")
        data = request.json
        client_name = "Demo Company"
        status_code = 200
        app.logger.info(f"Finished deletion of service plan: INFORMATION")
        return f"Service Plan Deleted: {client_name}", status_code

    @app.route("/refactor", methods=["POST"])
    def refactor_service_plan():
        app.logger.info("Starting refactor of service plan...")
        data = request.json
        client_name = "Demo Company"
        status_code = 200
        app.logger.info(f"Finished refactor of service plans: INFORMATION")
        return f"Service Plan Refactored: {client_name}", status_code

    @app.route("/update", methods=["POST"])
    def update_service_plans():
        app.logger.info("Starting update of service plans...")
        data = request.json
        client_name = ["Demo Company", "ACME Corp"]
        status_code = 200
        app.logger.info(f"Finished update of service plans: INFORMATION")
        return f"Service Plans Updated: {client_name}", status_code

    @app.route("/onboarding", methods=["POST"])
    def create_onboarding():
        app.logger.info("Starting creation of onboarding")
        data = request.json
        onboarding_status = CreateOnboarding(create_object=data, logger=app.logger)
        app.logger.info(f'Created onboarding for {data["client_name"]}')
        return (
            f'Service Plans Updated: {data["client_name"]}',
            onboarding_status.status_code,
        )

    @app.route("/favicon.ico")
    def favicon():
        return "", 204

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.error("Page not found")
        return jsonify(error=str(e)), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error("Server error")
        return jsonify(error=str(e)), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
