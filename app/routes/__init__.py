from flask import Blueprint, Flask
from app.routes.lead_route import bp as bp_lead

bp_api = Blueprint("api", __name__, url_prefix="")


def init_app(app: Flask):
    bp_api.register_blueprint(bp_lead)

    app.register_blueprint(bp_api)