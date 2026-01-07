from flask import Blueprint, request
from services.leadService import LeadService
from utils.response import success, error

lead_bp = Blueprint("leads", __name__)


@lead_bp.route("/", methods=["POST"])
def create_lead():
    data = request.get_json() or {}

    try:
        lead = LeadService.create_lead(data)
        return success("Lead criado com sucesso", lead.to_dict(), 201)

    except ValueError as e:
        return error(str(e), 400)

    except Exception:
        return error("Erro interno do servidor", 500)


@lead_bp.route("/", methods=["GET"])
def list_leads():
    try:
        filters = {
            "q": request.args.get("q"),
            "status": request.args.get("status"),
            "score_min": request.args.get("score_min"),
            "score_max": request.args.get("score_max"),
            "page": request.args.get("page", 1),
            "per_page": request.args.get("per_page", 10),
        }

        result = LeadService.list_leads(filters)
        return success("Leads listados com sucesso", result)

    except ValueError as e:
        return error(str(e), 400)

    except Exception:
        return error("Erro interno do servidor", 500)


@lead_bp.route("/<int:lead_id>", methods=["GET"])
def get_lead(lead_id):
    try:
        lead = LeadService.get_lead(lead_id)
        return success("Lead encontrado", lead.to_dict())

    except LookupError as e:
        return error(str(e), 404)

    except Exception:
        return error("Erro interno do servidor", 500)


@lead_bp.route("/<int:lead_id>", methods=["PUT"])
def update_lead(lead_id):
    data = request.get_json() or {}

    try:
        lead = LeadService.update_lead(lead_id, data)
        return success("Lead atualizado com sucesso", lead.to_dict())

    except ValueError as e:
        return error(str(e), 400)

    except LookupError as e:
        return error(str(e), 404)

    except Exception:
        return error("Erro interno do servidor", 500)


@lead_bp.route("/<int:lead_id>/status", methods=["PATCH"])
def update_status(lead_id):
    data = request.get_json() or {}
    new_status = data.get("status")

    try:
        lead = LeadService.update_status(lead_id, new_status)
        return success("Status atualizado com sucesso", lead.to_dict())

    except ValueError as e:
        return error(str(e), 400)

    except LookupError as e:
        return error(str(e), 404)

    except Exception:
        return error("Erro interno do servidor", 500)
