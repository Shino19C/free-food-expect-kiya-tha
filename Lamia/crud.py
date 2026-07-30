from datetime import datetime, timedelta, timezone

try:
    from .models import SOSReport
except ImportError:
    from models import SOSReport


def cleanup_expired_sos(db):
    now = datetime.now(timezone.utc)
    expired_reports = []

    for report in db.query(SOSReport).all():
        timestamp_value = getattr(report, "timestamp", "") or ""
        if not timestamp_value:
            continue

        try:
            parsed_timestamp = timestamp_value.replace("Z", "+00:00")
            parsed_time = datetime.fromisoformat(parsed_timestamp)
            if parsed_time.tzinfo is None:
                parsed_time = parsed_time.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

        if now - parsed_time > timedelta(hours=1):
            expired_reports.append(report)

    for report in expired_reports:
        db.delete(report)

    if expired_reports:
        db.commit()

    return len(expired_reports)


def create_sos(db, data):
    cleanup_expired_sos(db)

    report = SOSReport(**data.dict())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_all_sos(db):
    cleanup_expired_sos(db)
    return db.query(SOSReport).all()


def resolve_sos(db, report_id):
    cleanup_expired_sos(db)

    report = db.query(SOSReport).filter(
        SOSReport.id == report_id
    ).first()

    if report:
        report.status = "RESOLVED"
        db.commit()
        db.refresh(report)

    return report
