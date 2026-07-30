try:
    from .models import SOSReport
except ImportError:
    from models import SOSReport


def create_sos(db, data):
    report = SOSReport(**data.dict())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_all_sos(db):
    return db.query(SOSReport).all()


def resolve_sos(db, report_id):
    report = db.query(SOSReport).filter(
        SOSReport.id == report_id
    ).first()

    if report:
        report.status = "RESOLVED"
        db.commit()
        db.refresh(report)

    return report
