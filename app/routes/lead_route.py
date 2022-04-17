from flask import Blueprint
from app.controllers import lead_controller

bp = Blueprint("lead", __name__, url_prefix="/leads")


bp.post("")(lead_controller.create_lead)
bp.get("")(lead_controller.retrieve_leads)
bp.patch("")(lead_controller.add_visit)
bp.delete("")(lead_controller.delete_lead)
