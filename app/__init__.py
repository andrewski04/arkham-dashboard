from flask import Flask

# this defines the app that is created for the entrypoint (run.py) to run.

# Blueprints act like mini Flask apps that have separate routes and templates
# In this case, each API endpoint and the frontend are separate blueprints


def create_app():
    app = Flask(__name__)

    # API endpoints, the rest will be added when they are created
    from .api import network #, server, surveillance, biometric, physical, comms, threats
    app.register_blueprint(network.bp)


    # Frontend route
    from . import routes
    app.register_blueprint(routes.bp)

    return app
