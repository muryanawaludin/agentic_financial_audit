"""
Aplikasi Antarmuka Pengguna Streamlit:
Dasbor Audit Keuangan & Orkestrator Pemanggilan Perkakas (Tool Use & Function Calling).
© 2026 Muryan Awaludin. Seluruh hak cipta dilindungi undang-undang.
"""
import streamlit as st
import pandas as pd
import json
import os
from config import CONFIG
from agent.engine import AutonomousFinancialAuditAgent
from agent.tools import FinancialToolRegistry

# Konfigurasi Halaman Utama
st.set_page_config(
    page_title=CONFIG.APP_TITLE,
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Autonomous Financial Audit & ERP Reconciliation Agent")
st.caption("Penerapan Tool Use & Function Calling: Menghubungkan Logika Kognitif dengan Perkakas Aritmatika & Basis Data Deterministik")

# Inisialisasi Agen
if "audit_agent" not in st.session_state:
    st.session_state.audit_agent = AutonomousFinancialAuditAgent()

# Dataset Cadangan Mandiri (Fail-Safe) jika CSV fisik bermasalah
BACKUP_ERP_RECORDS = [
    {"transaction_id": "TX-9011", "timestamp": "2026-10-01 09:15:00", "vendor_id": "VND-801", "vendor_name": "PT Global Nusa Medika", "document_type": "INVOICE_SETTLEMENT", "invoice_amount": 15000000.0, "settled_amount": 15000000.0, "bank_fee": 0.0, "payment_reference": "PAY-REF-001", "status": "MATCHED"},
    {"transaction_id": "TX-9012", "timestamp": "2026-10-02 11:20:00", "vendor_id": "VND-802", "vendor_name": "CV Rekayasa Utama", "document_type": "INVOICE_SETTLEMENT", "invoice_amount": 8450000.0, "settled_amount": 8447500.0, "bank_fee": 2500.0, "payment_reference": "PAY-REF-002", "status": "MATCHED"},
    {"transaction_id": "TX-9013", "timestamp": "2026-10-03 14:05:00", "vendor_id": "VND-803", "vendor_name": "PT Sinar Logistik", "document_type": "DUPLICATE_PAYMENT", "invoice_amount": 4200000.0, "settled_amount": 4200000.0, "bank_fee": 0.0, "payment_reference": "PAY-REF-003", "status": "DUPLICATE_SUSPECT"},
    {"transaction_id": "TX-9014", "timestamp": "2026-10-03 14:06:12", "vendor_id": "VND-803", "vendor_name": "PT Sinar Logistik", "document_type": "DUPLICATE_PAYMENT", "invoice_amount": 4200000.0, "settled_amount": 4200000.0, "bank_fee": 0.0, "payment_reference": "PAY-REF-003", "status": "DUPLICATE_SUSPECT"},
    {"transaction_id": "TX-9015", "timestamp": "2026-10-04 16:45:00", "vendor_id": "VND-804", "vendor_name": "PT Mandiri Mega Sarana", "document_type": "INVOICE_SETTLEMENT", "invoice_amount": 27500000.0, "settled_amount": 27000000.0, "bank_fee": 0.0, "payment_reference": "PAY-REF-004", "status": "UNAPPLIED_VARIANCE"},
    {"transaction_id": "TX-9016", "timestamp": "2026-10-05 10:10:00", "vendor_id": "VND-805", "vendor_name": "PT Tirta Sentosa", "document_type": "INVOICE_SETTLEMENT", "invoice_amount": 12350750.0, "settled_amount": 12350000.0, "bank_fee": 0.0, "payment_reference": "PAY-REF-005", "status": "VARIANCE_DETECTED"}
]

def load_verified_erp_dataframe() -> pd.DataFrame:
    """Membaca CSV dengan deteksi otomatis pemisah kolom dan sanitasi skema."""
    csv_file = CONFIG.DATA_TRANSACTIONS_PATH
    
    if os.path.exists(csv_file):
        try:
            # Otomatis deteksi koma (,), titik koma (;), atau tab (\t)
            df = pd.read_csv(csv_file, sep=None, engine="python", encoding="utf-8-sig")
            
            # Bersihkan spasi dan normalkan ke huruf kecil
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            # Verifikasi ketersediaan kolom kunci
            if "vendor_id" in df.columns and "vendor_name" in df.columns:
                return df
        except Exception:
            pass  # Masuk ke fallback di bawah jika terjadi kegagalan baca

    # Jika berkas belum ada atau skemanya tidak sesuai, buat berkas baru secara otomatis
    df_fallback = pd.DataFrame(BACKUP_ERP_RECORDS)
    try:
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        df_fallback.to_csv(csv_file, index=False, encoding="utf-8")
    except Exception:
        pass
    return df_fallback

df_erp = load_verified_erp_dataframe()

# Sidebar: Pengaturan dan Pemilihan Skenario Audit
with st.sidebar:
    st.header("📋 Panel Pengujian Audit")
    st.markdown("Sumber Data: *ERP Financial Reconciliation Logs*")

    # Ambil vendor unik dengan validasi anti-error
    if not df_erp.empty and "vendor_id" in df_erp.columns and "vendor_name" in df_erp.columns:
        unique_vendors = df_erp[["vendor_id", "vendor_name"]].drop_duplicates().to_dict(orient="records")
    else:
        unique_vendors = [
            {"vendor_id": "VND-801", "vendor_name": "PT Global Nusa Medika"},
            {"vendor_id": "VND-802", "vendor_name": "CV Rekayasa Utama"},
            {"vendor_id": "VND-803", "vendor_name": "PT Sinar Logistik"},
            {"vendor_id": "VND-804", "vendor_name": "PT Mandiri Mega Sarana"},
            {"vendor_id": "VND-805", "vendor_name": "PT Tirta Sentosa"}
        ]

    selected_vendor_idx = st.selectbox(
        "Pilih Vendor untuk Diaudit:",
        range(len(unique_vendors)),
        format_func=lambda i: f"[{unique_vendors[i]['vendor_id']}] {unique_vendors[i]['vendor_name']}"
    )
    selected_vendor = unique_vendors[selected_vendor_idx]
    v_id = str(selected_vendor["vendor_id"])
    v_name = str(selected_vendor["vendor_name"])

    btn_audit = st.button("🚀 Jalankan Audit Berbasis Tool Use", type="primary", use_container_width=True)

    st.divider()
    st.markdown(f"**Target Vendor:** `{v_id}`")
    st.markdown(f"**Nama Perusahaan:** {v_name}")
    st.markdown(f"**Batas Toleransi Auto-Adjust:** `Rp {CONFIG.VARIANCE_TOLERANCE_THRESHOLD:,.2f}`")

    st.divider()
    st.markdown("© 2026 **Muryan Awaludin**  \nHak Cipta Dilindungi.")

# Area Kerja Utama
col_main, col_tools = st.columns([1.2, 0.8])

with col_tools:
    st.subheader("🛠️ Registri Perkakas (Tool Schemas)")
    st.caption("Kontrak formal JSON Schema yang diekspos ke agen:")
    tools_defs = FinancialToolRegistry.get_registered_tools_definitions()
    for td in tools_defs:
        with st.expander(f"🔧 `{td.name}`"):
            st.markdown(f"**Deskripsi:** {td.description}")
            st.markdown("**Skema Parameter (JSON Schema):**")
            st.code(json.dumps(td.parameters_schema, indent=2), language="json")

with col_main:
    st.subheader("🔍 Jejak Eksekusi Tool Calling")
    
    if btn_audit:
        with st.spinner(f"Agen sedang menganalisis buku besar {v_id} melalui pemanggilan perkakas..."):
            audit_report = st.session_state.audit_agent.audit_vendor_account(
                ticket_id=f"AUD-{v_id}-2026",
                vendor_id=v_id
            )
            st.session_state.audit_report = audit_report

    if "audit_report" in st.session_state and st.session_state.audit_report is not None:
        report = st.session_state.audit_report

        # Tampilkan Langkah Interaksi Alat
        for step in report.step_history:
            with st.container(border=True):
                st.markdown(f"**Iterasi {step.iteration}: Memanggil Perkakas `{step.tool_invoked}`**")
                st.markdown(f"🧠 **Rasional Kognitif:** *{step.rationale}*")
                st.markdown(f"📦 **Argumen JSON Dispatcher:**")
                st.code(json.dumps(step.arguments, indent=2), language="json")
                st.markdown(f"🔬 **Observasi Balik Lingkungan:**")
                st.code(json.dumps(step.observation, indent=2), language="json")

        st.divider()
        st.subheader("📊 Hasil Laporan Audit Rekonsiliasi")

        # Kartu Status Putusan
        if report.reconciliation_verdict == "FULLY_RECONCILED":
            st.success("✅ **STATUS: REKONSILIASI PENUH (BALANCE TEPAT)**")
        elif report.reconciliation_verdict == "AUTO_ADJUSTED":
            st.info(f"🔄 **STATUS: SELESAI DENGAN PENYESUAIAN OTOMATIS (ID: {report.adjustment_entry_id})**")
        else:
            st.error("⚠️ **STATUS: DILAPORKAN KE AUDITOR MANUSIA (DISPARITAS TINGGI / DUPLIKASI)**")

        # Ringkasan Angka Finansial
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Faktur", f"Rp {report.total_invoice_sum:,.2f}")
        c2.metric("Total Kas Masuk", f"Rp {report.total_settled_sum:,.2f}")
        c3.metric("Varians Bersih", f"Rp {report.net_variance_amount:,.2f}")

        st.markdown("**Catatan Temuan Anomali & Rekomendasi:**")
        for reason in report.discrepancy_reasons:
            st.warning(f"• {reason}")
    else:
        st.info("Pilih entitas vendor pada bilah sisi kiri lalu tekan tombol **'Jalankan Audit Berbasis Tool Use'**.")

st.divider()
st.caption(CONFIG.AUTHOR_COPYRIGHT)