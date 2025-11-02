# app/core/rate_limit.py
from datetime import datetime, timedelta
from fastapi import HTTPException, status

def check_rate_limit(db, ip_address: str, endpoint: str, limit_per_day: int = 3):
    from app.models.rate_limit import RateLimit
    now = datetime.utcnow()
    reset_time = now - timedelta(days=1)

    record = (
        db.query(RateLimit)
        .filter(RateLimit.ip_address == ip_address, RateLimit.endpoint == endpoint)
        .first()
    )

    if not record:
        record = RateLimit(ip_address=ip_address, endpoint=endpoint, count=1)
        db.add(record)
        db.commit()
        return

    # Reset after 24 hours
    if record.last_request < reset_time:
        record.count = 1
        record.last_request = now
    else:
        if record.count >= limit_per_day:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Daily limit reached. Please register or try again tomorrow.",
            )
        record.count += 1
        record.last_request = now

    db.commit()
