from flask import Flask, jsonify
import os
import logging

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    
    # setup logging
    logging.basicConfig(level=logging.DEBUG)
    
    @app.route('/')
    def hello_world():
        app.logger.info('Processing default request')
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
