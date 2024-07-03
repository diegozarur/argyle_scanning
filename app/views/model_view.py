from typing import Optional, Any, Dict
from flask import jsonify, Response


class ModelView:

    @staticmethod
    def success(data: Optional[Dict[str, Any]] = None) -> Response:
        return jsonify({"success": True, "data": data or {}})

    @staticmethod
    def error(error: Optional[str] = None) -> Response:
        return jsonify({"success": False, "error": error})

    @staticmethod
    def message_result(data: Any) -> Dict[str, Any]:
        return {
            "state": data.state,
            "result": data.result if data.state != "FAILURE" else str(data.result),
        }
