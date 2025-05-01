# routes/modules_router.py
from flask import Blueprint, jsonify
from models.module import Module

modules_bp = Blueprint('modules', __name__)


@modules_bp.route("/modules/all", methods=["GET"])
def get_modules():
    modules = Module.query.all()
    return jsonify({"success": True, "message": "Modules retrieved successfully",
                    "modules": [module.to_dict() for module in modules]}), 200
