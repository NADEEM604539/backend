from db import SessionLocal
from models import IssueRecord, IssueStatus

db = SessionLocal()
issue = db.query(IssueRecord).filter(IssueRecord.issue_id == 1).first()
if issue:
    # Reset to APPROVED without returned_at so we can trigger the return endpoint
    issue.status = IssueStatus.APPROVED
    issue.returned_at = None
    issue.fine_amount = 0
    issue.late_days = 0
    db.commit()
    print("✓ Issue reset to APPROVED status")
db.close()
