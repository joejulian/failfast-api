import os
from flask import Flask, request
from flask_cors import CORS


def getvalues():
    jsonbody = request.get_json(force=True, silent=True)
    values = request.values.to_dict()
    if jsonbody:
        values.update(jsonbody)
    return values


def create_app():
    app = Flask(__name__)
    CORS(app)
    setting = os.getenv('APP_ENV', "development")
    if setting != 'production':
        app.config.from_object('hub2labhook.api.config.DevelopmentConfig')
    else:
        app.config.from_object('hub2labhook.api.config.ProductionConfig')
    from hub2labhook.api.info import info_app
    from hub2labhook.api.hook import hook_app
    app.register_blueprint(info_app, url_prefix='')
    app.register_blueprint(hook_app, url_prefix='')
    app.logger.info("Start service")
    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host='0.0.0.0')
