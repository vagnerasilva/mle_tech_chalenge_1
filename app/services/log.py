import json
import uuid
from datetime import datetime, timezone

from fastapi import Request
from starlette.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.logs import ApiLog


def write_log(
    req: Request, res: StreamingResponse, req_body: dict, res_body: str, process_time: float):
    db = next(get_db())

    try:
        res_body = json.loads(res_body)
    except Exception:
        res_body = None

    log = ApiLog(
        api_key=uuid.UUID(req.headers.get("x-api-key")) if req.headers.get("x-api-key") else None,
        ip_address=req.client.host,
        path=req.url.path,
        method=req.method,
        status_code=res.status_code,
        request_body=req_body,
        response_body=res_body,
        query_params=dict(req.query_params),
        path_params=req.path_params,
        process_time=process_time,
        created_at=datetime.now(timezone.utc)
    )
    db.add(log)
    db.commit()

    db.close()


def get_logs(db: Session) -> list:
    logs = db.query(ApiLog).all()
    return logs
