"""
Skrip Otomasi Pembuatan Basis Data Transaksi ERP untuk Bab 4.
© 2026 Muryan Awaludin.
"""
import os
import pandas as pd

# Pastikan folder data/ tersedia
os.makedirs("data", exist_ok=True)

data = [
    {
        "transaction_id": "TX-9011",
        "timestamp": "2026-10-01 09:15:00",
        "vendor_id": "VND-801",
        "vendor_name": "PT Global Nusa Medika",
        "document_type": "INVOICE_SETTLEMENT",
        "invoice_amount": 15000000.0,
        "settled_amount": 15000000.0,
        "bank_fee": 0.0,
        "payment_reference": "PAY-REF-001",
        "status": "MATCHED"
    },
    {
        "transaction_id": "TX-9012",
        "timestamp": "2026-10-02 11:20:00",
        "vendor_id": "VND-802",
        "vendor_name": "CV Rekayasa Utama",
        "document_type": "INVOICE_SETTLEMENT",
        "invoice_amount": 8450000.0,
        "settled_amount": 8447500.0,
        "bank_fee": 2500.0,
        "payment_reference": "PAY-REF-002",
        "status": "MATCHED"
    },
    {
        "transaction_id": "TX-9013",
        "timestamp": "2026-10-03 14:05:00",
        "vendor_id": "VND-803",
        "vendor_name": "PT Sinar Logistik",
        "document_type": "DUPLICATE_PAYMENT",
        "invoice_amount": 4200000.0,
        "settled_amount": 4200000.0,
        "bank_fee": 0.0,
        "payment_reference": "PAY-REF-003",
        "status": "DUPLICATE_SUSPECT"
    },
    {
        "transaction_id": "TX-9014",
        "timestamp": "2026-10-03 14:06:12",
        "vendor_id": "VND-803",
        "vendor_name": "PT Sinar Logistik",
        "document_type": "DUPLICATE_PAYMENT",
        "invoice_amount": 4200000.0,
        "settled_amount": 4200000.0,
        "bank_fee": 0.0,
        "payment_reference": "PAY-REF-003",
        "status": "DUPLICATE_SUSPECT"
    },
    {
        "transaction_id": "TX-9015",
        "timestamp": "2026-10-04 16:45:00",
        "vendor_id": "VND-804",
        "vendor_name": "PT Mandiri Mega Sarana",
        "document_type": "INVOICE_SETTLEMENT",
        "invoice_amount": 27500000.0,
        "settled_amount": 27000000.0,
        "bank_fee": 0.0,
        "payment_reference": "PAY-REF-004",
        "status": "UNAPPLIED_VARIANCE"
    },
    {
        "transaction_id": "TX-9016",
        "timestamp": "2026-10-05 10:10:00",
        "vendor_id": "VND-805",
        "vendor_name": "PT Tirta Sentosa",
        "document_type": "INVOICE_SETTLEMENT",
        "invoice_amount": 12350750.0,
        "settled_amount": 12350000.0,
        "bank_fee": 0.0,
        "payment_reference": "PAY-REF-005",
        "status": "VARIANCE_DETECTED"
    },
    {
        "transaction_id": "TX-9017",
        "timestamp": "2026-10-06 08:30:00",
        "vendor_id": "VND-801",
        "vendor_name": "PT Global Nusa Medika",
        "document_type": "INVOICE_SETTLEMENT",
        "invoice_amount": 6500000.0,
        "settled_amount": 6500000.0,
        "bank_fee": 0.0,
        "payment_reference": "PAY-REF-006",
        "status": "MATCHED"
    },
    {
        "transaction_id": "TX-9018",
        "timestamp": "2026-10-06 13:45:00",
        "vendor_id": "VND-806",
        "vendor_name": "PT Samudera Logistik Nusantara",
        "document_type": "INVOICE_SETTLEMENT",
        "invoice_amount": 18200000.0,
        "settled_amount": 18200000.0,
        "bank_fee": 0.0,
        "payment_reference": "PAY-REF-007",
        "status": "MATCHED"
    },
    {
        "transaction_id": "TX-9019",
        "timestamp": "2026-10-07 15:10:00",
        "vendor_id": "VND-805",
        "vendor_name": "PT Tirta Sentosa",
        "document_type": "INVOICE_SETTLEMENT",
        "invoice_amount": 5400300.0,
        "settled_amount": 5400000.0,
        "bank_fee": 0.0,
        "payment_reference": "PAY-REF-008",
        "status": "VARIANCE_DETECTED"
    },
    {
        "transaction_id": "TX-9020",
        "timestamp": "2026-10-08 17:25:00",
        "vendor_id": "VND-802",
        "vendor_name": "CV Rekayasa Utama",
        "document_type": "INVOICE_SETTLEMENT",
        "invoice_amount": 11200000.0,
        "settled_amount": 11197500.0,
        "bank_fee": 2500.0,
        "payment_reference": "PAY-REF-009",
        "status": "MATCHED"
    }
]

df = pd.DataFrame(data)
csv_path = os.path.join("data", "erp_financial_transactions.csv")
df.to_csv(csv_path, index=False, encoding="utf-8")
print(f"File database berhasil dibuat di: {os.path.abspath(csv_path)}")
print(f"Total baris: {len(df)}")