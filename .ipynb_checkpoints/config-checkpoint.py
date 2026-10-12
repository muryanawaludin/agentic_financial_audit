"""
Konfigurasi Global Sistem Audit Keuangan dan Pemanggilan Perkakas Agen.
© 2026 Muryan Awaludin. Seluruh hak cipta dilindungi undang-undang.
"""
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class FinancialAuditConfig:
    APP_TITLE: str = "Autonomous Financial Audit & ERP Reconciliation Agent"
    AUTHOR_COPYRIGHT: str = "© 2026 Muryan Awaludin. Seluruh hak cipta dilindungi undang-undang."
    DATA_TRANSACTIONS_PATH: str = os.path.join(os.path.dirname(__file__), "data", "erp_financial_transactions.csv")
    
    # Ambang Batas Toleransi Selisih Audit (Discrepancy Threshold) dalam Rupiah/Valuta
    VARIANCE_TOLERANCE_THRESHOLD: float = 1000.0  # Selisih di bawah ini dapat di-adjust otomatis
    MAX_RECONCILIATION_LOOPS: int = 4

CONFIG = FinancialAuditConfig()