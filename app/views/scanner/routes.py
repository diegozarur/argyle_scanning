from typing import Tuple, Any
from flask import Response, url_for
from app.views.scanner import blueprint
from app.views.model_view import ModelView
from app.views.scanner.tasks import scanner_task
from celery.result import AsyncResult



@blueprint.route("/<name>", methods=["POST"])
def scanner(name: str) -> Tuple[Response, int]:
    try:
        result = scanner_task.delay(scanner_name=name)
        status_url = url_for('scanner_blueprint.scanner_status', message_id=result.task_id, _external=True)
        return (
            ModelView.success(
                data={
                    'state': result.state,
                    'task_id': result.task_id,
                    'url': status_url
                }
            ),
            200,
        )
    except Exception as e:
        return ModelView.error(error=str(e)), 500


@blueprint.route("/status/<message_id>", methods=["GET"])
def scanner_status(message_id: str) -> tuple[dict[str, Any], int]:
    result = AsyncResult(message_id)

    return ModelView.message_result(data=result), 200
