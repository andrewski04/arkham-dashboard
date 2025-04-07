from flask import Flask

# this defines the app that is created for the entrypoint (run.py) to run.

# Blueprints act like mini Flask apps that have separate routes and templates
# In this case, each API endpoint and the frontend are separate blueprints


def create_app():
    app = Flask(__name__)

    # API endpoints, the rest will be added when they are created
    from .api import network, server_logs, video_surveillance, biometric_access, physical_security, internal_comms, inmate_threats
    app.register_blueprint(network.bp)
    app.register_blueprint(server_logs.bp)
    app.register_blueprint(video_surveillance.bp)
    app.register_blueprint(biometric_access.bp)
    app.register_blueprint(physical_security.bp)
    app.register_blueprint(internal_comms.bp)
    app.register_blueprint(inmate_threats.bp)

    # Frontend route
    from . import routes
    app.register_blueprint(routes.bp)

    return app
