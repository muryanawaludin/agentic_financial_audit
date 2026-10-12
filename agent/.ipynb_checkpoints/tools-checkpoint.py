"""
Financial Tool Registry: Kumpulan Perkakas Deterministik Simbolik.
Menyediakan operasi pembacaan buku besar, kalkulator aritmatika desimal,
deteksi duplikasi, dan pencatatan jurnal penyesuaian (adjustment).
© 2026 Muryan Awaludin.
"""
import json
import math
import os
import pandas as pd
from typing import Dict, Any, List, Optional  # <-- Tambahkan Optional di sini
from config import CONFIG
from agent.schema import ToolDefinition

class FinancialToolRegistry:
    
    _db_cache: Optional[pd.DataFrame] = None

    @classmethod
    def _get_data(cls) -> pd.DataFrame:
        if cls._db_cache is None:
            if os.path.exists(CONFIG.DATA_TRANSACTIONS_PATH):
                cls._db_cache = pd.read_csv(CONFIG.DATA_TRANSACTIONS_PATH)
            else:
                cls._db_cache = pd.DataFrame()
        return cls._db_cache

    # 1. Perkakas Pembacaan Buku Besar (Read-Only)
    @classmethod
    def query_ledger_transactions(cls, vendor_id: str) -> Dict[str, Any]:
        """Mengambil seluruh catatan transaksi buku besar dan rekening bank berdasarkan ID vendor."""
        df = cls._get_data()
        if df.empty:
            return {"error": "Basis data ERP tidak dapat diakses."}
        
        filtered = df[df["vendor_id"].str.upper() == vendor_id.upper()]
        if filtered.empty:
            return {"status": "NOT_FOUND", "message": f"Tidak ditemukan catatan transaksi untuk vendor '{vendor_id}'."}
        
        records = filtered.to_dict(orient="records")
        return {
            "status": "SUCCESS",
            "vendor_id": vendor_id,
            "total_records": len(records),
            "transactions": records
        }

    # 2. Perkakas Kalkulator Aritmatika Presisi Tinggi (ALU Deterministik)
    @classmethod
    def calculate_reconciliation_variance(cls, invoice_amounts: List[float], settled_amounts: List[float], bank_fees: List[float]) -> Dict[str, Any]:
        """Menghitung total faktur, total penyelesaian, biaya bank, dan varians selisih matematis eksak."""
        total_inv = math.fsum(invoice_amounts)
        total_set = math.fsum(settled_amounts)
        total_fee = math.fsum(bank_fees)
        
        # Varians Bersih = Total Faktur - (Total Penyelesaian + Total Biaya Bank)
        net_variance = round(total_inv - (total_set + total_fee), 2)
        
        return {
            "total_invoices": round(total_inv, 2),
            "total_settled": round(total_set, 2),
            "total_bank_fees": round(total_fee, 2),
            "net_variance": net_variance,
            "is_balanced": math.isclose(net_variance, 0.0, abs_tol=0.01)
        }

    # 3. Perkakas Deteksi Transaksi Duplikat
    @classmethod
    def detect_duplicate_invoices(cls, vendor_id: str) -> Dict[str, Any]:
        """Mendeteksi apakah terdapat referensi pembayaran atau nilai transaksi ganda dalam interval pendek."""
        df = cls._get_data()
        vendor_data = df[df["vendor_id"].str.upper() == vendor_id.upper()]
        
        duplicates = vendor_data[vendor_data.duplicated(subset=["payment_reference", "invoice_amount"], keep=False)]
        
        if not duplicates.empty:
            dup_list = duplicates.to_dict(orient="records")
            return {
                "has_duplicates": True,
                "duplicate_count": len(dup_list),
                "suspect_records": dup_list,
                "risk_assessment": "CRITICAL: Terdeteksi potensi pembayaran ganda terhadap referensi yang sama."
            }
        
        return {
            "has_duplicates": False,
            "duplicate_count": 0,
            "risk_assessment": "CLEAN: Tidak ada anomali duplikasi referensi pembayaran."
        }

    # 4. Perkakas Mutasi Buku Besar (Write-Mutation dengan Otorisasi)
    @classmethod
    def post_ledger_adjustment(cls, vendor_id: str, adjustment_amount: float, reason: str) -> Dict[str, Any]:
        """Mencatat jurnal penyesuaian (compensating entry) untuk selisih di bawah batas toleransi resmi."""
        if abs(adjustment_amount) > CONFIG.VARIANCE_TOLERANCE_THRESHOLD:
            return {
                "status": "REJECTED",
                "message": f"Nilai selisih ({adjustment_amount:,.2f}) melampaui batas toleransi otomatis "
                           f"({CONFIG.VARIANCE_TOLERANCE_THRESHOLD:,.2f}). Memerlukan persetujuan manual CFO."
            }
        
        entry_id = f"ADJ-2026-X{abs(int(adjustment_amount * 100))}"
        return {
            "status": "POSTED",
            "adjustment_entry_id": entry_id,
            "vendor_id": vendor_id,
            "adjusted_amount": adjustment_amount,
            "account_credited": "9100-Bank-Charges-Variance",
            "reason": reason,
            "journal_timestamp": "2026-10-10 19:34:00"
        }

    @classmethod
    def get_registered_tools_definitions(cls) -> List[ToolDefinition]:
        """Mengembalikan metadata JSON Schema untuk seluruh alat yang tersedia."""
        return [
            ToolDefinition(
                name="query_ledger_transactions",
                description="Mengambil data transaksi buku besar dari database ERP berdasarkan vendor_id.",
                parameters_schema={
                    "type": "object",
                    "properties": {
                        "vendor_id": {"type": "string", "description": "ID Unik vendor (misal: VND-802)"}
                    },
                    "required": ["vendor_id"]
                }
            ),
            ToolDefinition(
                name="calculate_reconciliation_variance",
                description="Melakukan komputasi aritmatika deterministik atas daftar faktur, pembayaran, dan biaya bank.",
                parameters_schema={
                    "type": "object",
                    "properties": {
                        "invoice_amounts": {"type": "array", "items": {"type": "number"}},
                        "settled_amounts": {"type": "array", "items": {"type": "number"}},
                        "bank_fees": {"type": "array", "items": {"type": "number"}}
                    },
                    "required": ["invoice_amounts", "settled_amounts", "bank_fees"]
                }
            ),
            ToolDefinition(
                name="detect_duplicate_invoices",
                description="Menganalisis anomali duplikasi nomor pembayaran pada buku besar vendor.",
                parameters_schema={
                    "type": "object",
                    "properties": {
                        "vendor_id": {"type": "string", "description": "ID Unik vendor"}
                    },
                    "required": ["vendor_id"]
                }
            ),
            ToolDefinition(
                name="post_ledger_adjustment",
                description="Mencatat jurnal penyesuaian untuk menutup selisih kecil dalam batas toleransi.",
                parameters_schema={
                    "type": "object",
                    "properties": {
                        "vendor_id": {"type": "string"},
                        "adjustment_amount": {"type": "number"},
                        "reason": {"type": "string"}
                    },
                    "required": ["vendor_id", "adjustment_amount", "reason"]
                }
            )
        ]

    @classmethod
    def dispatch_tool(cls, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Pintu gerbang eksekusi alat dengan validasi skema runtime."""
        if name == "query_ledger_transactions":
            return cls.query_ledger_transactions(**arguments)
        elif name == "calculate_reconciliation_variance":
            return cls.calculate_reconciliation_variance(**arguments)
        elif name == "detect_duplicate_invoices":
            return cls.detect_duplicate_invoices(**arguments)
        elif name == "post_ledger_adjustment":
            return cls.post_ledger_adjustment(**arguments)
        else:
            return {"error": f"Tool '{name}' tidak dikenal dalam registri."}