"""
Skema Pydantic untuk Deklarasi Kontrak JSON Schema Perkakas dan Hasil Audit.
© 2026 Muryan Awaludin.
"""
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

class ToolDefinition(BaseModel):
    name: str = Field(..., description="Nama unik fungsi perkakas")
    description: str = Field(..., description="Dokumentasi fungsi dan kasus penggunaannya")
    parameters_schema: Dict[str, Any] = Field(..., description="Skema JSON formal argumen fungsi")

class ToolCallRequest(BaseModel):
    call_id: str
    tool_name: str
    arguments: Dict[str, Any]

class ToolExecutionResult(BaseModel):
    call_id: str
    tool_name: str
    is_success: bool
    payload: Dict[str, Any]
    error_message: Optional[str] = None

class ReconciliationStep(BaseModel):
    iteration: int
    rationale: str
    tool_invoked: str
    arguments: Dict[str, Any]
    observation: Dict[str, Any]

class AuditReconciliationReport(BaseModel):
    audit_ticket_id: str
    vendor_id: str
    vendor_name: str
    transactions_audited_count: int
    total_invoice_sum: float
    total_settled_sum: float
    net_variance_amount: float
    reconciliation_verdict: Literal["FULLY_RECONCILED", "AUTO_ADJUSTED", "FLAGGED_FOR_HUMAN_AUDITOR"]
    discrepancy_reasons: List[str]
    adjustment_entry_id: Optional[str] = None
    step_history: List[ReconciliationStep]