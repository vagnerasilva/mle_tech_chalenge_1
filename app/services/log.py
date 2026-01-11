import json
import uuid
from datetime import datetime, timezone

from fastapi import Request
from starlette.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.logs import ApiLog


def write_log(
    req: Request,
    res: StreamingResponse, 
    req_body: dict, 
    res_body: str, 
    process_time: float
    ):
    db = next(get_db())

    try:
        log = ApiLog(
            ip_address=req.client.host if req.client else None,
            path=req.url.path,
            method=req.method,
            status_code=res.status_code,
            process_time=process_time,
            created_at=datetime.utcnow(),
        )
        db.add(log)
        db.commit()
    finally:
        db.close()


def get_logs(db: Session) -> list:
    logs = db.query(ApiLog).all()
    result = []
    for l in logs:
        result.append({
            "id": l.id,
            "method": l.method,
            "path": l.path,
            "status_code": l.status_code,
            "process_time": l.process_time,
            "ip_address": l.ip_address,
            "created_at": l.created_at.isoformat() if l.created_at else None,
        })
    return result
