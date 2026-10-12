"""
Orkestrator Function Calling dan Penalaran Siklis Audit Keuangan.
Mengeksekusi siklus penalaran, memanggil perkakas yang sesuai, dan menyusun laporan audit formal.
© 2026 Muryan Awaludin.
"""
import json
from typing import List, Dict, Any
from config import CONFIG
from agent.schema import ReconciliationStep, AuditReconciliationReport
from agent.tools import FinancialToolRegistry

class AutonomousFinancialAuditAgent:
    
    def __init__(self):
        self.tool_definitions = FinancialToolRegistry.get_registered_tools_definitions()

    def audit_vendor_account(self, ticket_id: str, vendor_id: str) -> AuditReconciliationReport:
        step_history: List[ReconciliationStep] = []
        discrepancy_reasons: List[str] = []
        adjustment_entry_id = None
        
        # Iterasi 1: Pengambilan Data Buku Besar (Query Ledger)
        r1 = f"Langkah 1: Menarik seluruh catatan transaksi buku besar dan penyelesaian untuk vendor {vendor_id}."
        args1 = {"vendor_id": vendor_id}
        obs1 = FinancialToolRegistry.dispatch_tool("query_ledger_transactions", args1)
        step_history.append(ReconciliationStep(
            iteration=1,
            rationale=r1,
            tool_invoked="query_ledger_transactions",
            arguments=args1,
            observation=obs1
        ))

        transactions = obs1.get("transactions", [])
        if not transactions:
            return AuditReconciliationReport(
                audit_ticket_id=ticket_id,
                vendor_id=vendor_id,
                vendor_name="Unknown",
                transactions_audited_count=0,
                total_invoice_sum=0.0,
                total_settled_sum=0.0,
                net_variance_amount=0.0,
                reconciliation_verdict="FLAGGED_FOR_HUMAN_AUDITOR",
                discrepancy_reasons=["Data transaksi tidak ditemukan pada basis data ERP."],
                step_history=step_history
            )

        vendor_name = transactions[0].get("vendor_name", "Vendor Terdaftar")

        # Iterasi 2: Deteksi Duplikasi Pembayaran
        r2 = f"Langkah 2: Memeriksa integritas pembayaran terhadap indikasi transaksi ganda (duplicate transactions)."
        args2 = {"vendor_id": vendor_id}
        obs2 = FinancialToolRegistry.dispatch_tool("detect_duplicate_invoices", args2)
        step_history.append(ReconciliationStep(
            iteration=2,
            rationale=r2,
            tool_invoked="detect_duplicate_invoices",
            arguments=args2,
            observation=obs2
        ))

        has_duplicates = obs2.get("has_duplicates", False)
        if has_duplicates:
            discrepancy_reasons.append("Terdeteksi duplikasi pembayaran ganda pada sistem perbankan.")

        # Iterasi 3: Komputasi Varians Aritmatika Deterministik
        invoices = [float(t["invoice_amount"]) for t in transactions]
        settled = [float(t["settled_amount"]) for t in transactions]
        fees = [float(t["bank_fee"]) for t in transactions]

        r3 = f"Langkah 3: Menjalankan kalkulator deterministik untuk menghitung selisih faktur vs kas masuk."
        args3 = {"invoice_amounts": invoices, "settled_amounts": settled, "bank_fees": fees}
        obs3 = FinancialToolRegistry.dispatch_tool("calculate_reconciliation_variance", args3)
        step_history.append(ReconciliationStep(
            iteration=3,
            rationale=r3,
            tool_invoked="calculate_reconciliation_variance",
            arguments=args3,
            observation=obs3
        ))

        net_variance = obs3.get("net_variance", 0.0)
        total_inv = obs3.get("total_invoices", 0.0)
        total_set = obs3.get("total_settled", 0.0)
        total_fee = obs3.get("total_bank_fees", 0.0)

        # Iterasi 4: Evaluasi Rekonsiliasi & Jurnal Penyesuaian
        if obs3.get("is_balanced") and not has_duplicates:
            verdict = "FULLY_RECONCILED"
        elif abs(net_variance) <= CONFIG.VARIANCE_TOLERANCE_THRESHOLD and not has_duplicates and abs(net_variance) > 0.0:
            # Otomatisasi penyesuaian buku besar untuk selisih kecil (misal biaya admin bank selisih pembulatan)
            r4 = f"Langkah 4: Selisih Rp {net_variance:,.2f} berada dalam batas toleransi. Melakukan posting jurnal penyesuaian."
            args4 = {
                "vendor_id": vendor_id,
                "adjustment_amount": net_variance,
                "reason": f"Penyelarasan selisih pembulatan dan administrasi bank untuk vendor {vendor_id}."
            }
            obs4 = FinancialToolRegistry.dispatch_tool("post_ledger_adjustment", args4)
            step_history.append(ReconciliationStep(
                iteration=4,
                rationale=r4,
                tool_invoked="post_ledger_adjustment",
                arguments=args4,
                observation=obs4
            ))
            adjustment_entry_id = obs4.get("adjustment_entry_id")
            verdict = "AUTO_ADJUSTED"
            discrepancy_reasons.append(f"Selisih administrasi bank Rp {net_variance:,.2f} diselesaikan via jurnal penyesuaian.")
        else:
            verdict = "FLAGGED_FOR_HUMAN_AUDITOR"
            if abs(net_variance) > CONFIG.VARIANCE_TOLERANCE_THRESHOLD:
                discrepancy_reasons.append(f"Varians tak teralokasi sebesar Rp {net_variance:,.2f} melampaui batas toleransi otomatis.")

        return AuditReconciliationReport(
            audit_ticket_id=ticket_id,
            vendor_id=vendor_id,
            vendor_name=vendor_name,
            transactions_audited_count=len(transactions),
            total_invoice_sum=total_inv,
            total_settled_sum=total_set,
            net_variance_amount=net_variance,
            reconciliation_verdict=verdict,
            discrepancy_reasons=discrepancy_reasons if discrepancy_reasons else ["Seluruh transaksi seimbang dan valid."],
            adjustment_entry_id=adjustment_entry_id,
            step_history=step_history
        )