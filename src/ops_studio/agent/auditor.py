from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class AuditRecord:
    correlation_id: str
    action: str
    agent_id: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    result: str = ""
    approved_by: Optional[str] = None
    details: dict = field(default_factory=dict)


class Auditor:
    """บันทึกทุก action ที่ Agent ทำ - immutable log"""

    def __init__(self):
        self.records: list[AuditRecord] = []

    async def log_action(
        self,
        correlation_id: str,
        action: str,
        agent_id: str,
        result: str = "",
        approved_by: Optional[str] = None,
        details: Optional[dict] = None,
    ) -> AuditRecord:
        record = AuditRecord(
            correlation_id=correlation_id,
            action=action,
            agent_id=agent_id,
            result=result,
            approved_by=approved_by,
            details=details or {},
        )
        self.records.append(record)
        return record

    def get_records(self, correlation_id: Optional[str] = None) -> list[AuditRecord]:
        if correlation_id:
            return [r for r in self.records if r.correlation_id == correlation_id]
        return self.records