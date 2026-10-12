# Autonomous Financial Audit & ERP Reconciliation Agent
### Bab 4: Tool Use dan Function Calling: Menghubungkan Logika LLM dengan Dunia Nyata

[![Demo Aplikasi](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sgentic-financial-audit.streamlit.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-agentic__financial__audit-blue?logo=github)](https://github.com/muryanawaludin/agentic_financial_audit.git)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/Copyright-©%202026%20Muryan%20Awaludin-green)](LICENSE)

Repositori ini memuat implementasi lengkap dari **Bab 4** buku rekayasa Agentic AI, yang berfokus pada integrasi logika kognitif *Large Language Models* (LLM) dengan dunia komputasi deterministik melalui **Tool Use** dan **Function Calling**. 

Sistem ini merealisasikan agen otonom untuk audit transaksi keuangan enterprise dan rekonsiliasi data *Enterprise Resource Planning* (ERP), menjamin integritas kalkulasi matematis tanpa risiko halusinasi desimal serta menyediakan jejak audit (*audit trail*) transparan.

---

## 🌐 Demo Aplikasi Interaktif

Aplikasi ini telah dikonfigurasi agar dapat langsung diuji coba secara publik tanpa instalasi lokal:

👉 **[Buka Demo Aplikasi Streamlit](https://sgentic-financial-audit.streamlit.app)**  
*(URL alternatif: [https://agentic_financial_audit.streamlit.app](https://sgentic-financial-audit.streamlit.app))*

---

## 🔬 Latar Belakang & Landasan Teori

Model bahasa autoregresif murni memprediksi token berdasarkan pemetaan probabilitas statistik:

$$P(w_1, w_2, \dots, w_T) = \prod_{t=1}^T P(w_t \mid w_1, \dots, w_{t-1})$$

Sifat komputasi probabilistik ini menimbulkan tiga kelemahan fatal pada sistem audit perbankan dan akuntansi:
1. **Kegagalan Aritmatika Desimal Presisi:** Ketiadaan unit logika aritmatika (*Arithmetic Logic Unit* / ALU) memicu kesalahan pembulatan (*off-by-one errors*) dan halusinasi angka.
2. **Ketiadaan Status Waktu-Nyata (*Knowledge Cutoff*):** Model tidak dapat mengamati mutasi saldo kas riil atau status transaksi terkini.
3. **Ketiadaan Daya Ubah Status Lingkungan (*Zero Side-Effects*):** Model teks pasif tidak memiliki otoritas menerbitkan mutasi buku besar atau memanggil *stored procedure* SQL.

### Paradigma Tool-Augmented & Function Calling
Untuk memecahkan kendala di atas, agen dialihfungsikan menjadi **pengendali kognitif (*cognitive dispatcher*)** yang memanfaatkan kontrak antarmuka formal berbasis **JSON Schema** dan validasi skema Pydantic:

$$\pi_\theta(c_t) \to \left( f^*, \mathbf{p}^* \right)$$

Di mana:
- $f^* \in \mathcal{T} \cup \{\text{TERMINATE}\}$ adalah perkakas terpilih dari registri $\mathcal{T}$.
- $\mathbf{p}^*$ adalah vektor argumen parameter yang divalidasi oleh operator deterministik $\mathcal{V}(\mathbf{p}^*, \mathcal{S}_{f^*})$.

---

## 🛠️ Registri Perkakas Deterministik (Tool Registry)

Sistem mengisolasi eksekusi perkakas melalui empat instrumen simbolik:

| Nama Perkakas | Kategori | Deskripsi Fungsional |
| :--- | :--- | :--- |
| `query_ledger_transactions` | *Read-Only* | Menarik seluruh riwayat transaksi buku besar dan rekening bank berdasarkan `vendor_id`. |
| `calculate_reconciliation_variance` | *ALU Deterministik* | Komputasi varians eksak: $\text{Varians} = \sum \text{Faktur} - (\sum \text{Kas Terbayar} + \sum \text{Biaya Bank})$. |
| `detect_duplicate_invoices` | *Audit Anomali* | Mendeteksi pembayaran ganda berdasarkan referensi pembayaran dan nominal identik. |
| `post_ledger_adjustment` | *Write-Mutation* | Menerbitkan jurnal penyesuaian jika selisih berada di bawah ambang batas toleransi resmi (Rp 1.000,00). |

---

## 🏗️ Alur Arsitektur Sistem

```
                                  ┌────────────────────────────────────────┐
                                  │      AUDIT INQUIRY / TIKET REKONSILIASI│
                                  │   "Verifikasi Transaksi Vendor V-904"  │
                                  └───────────────────┬────────────────────┘
                                                      │
                                                      ▼
                                  ┌────────────────────────────────────────┐
                         ┌───────►│       AGENT COGNITIVE CONTROLLER       │◄──────┐
                         │        │  - Menganalisis Dokumen Masuk          │       │
                         │        │  - Menentukan Urutan Eksekusi Tool     │       │
                         │        └───────────────────┬────────────────────┘       │
                         │                            │                            │
                         │          Panggil Tool      │ Hasil Observasi Valid      │
                         │          + JSON Schema     │                            │
                         │                            ▼                            │
                         │        ┌────────────────────────────────────────┐       │
                         │        │     FUNCTION DISPATCHER & GATEWAY      │       │
                         │        │  - Sanitasi Input & Batas Otorisasi    │       │
                         │        │  - Validasi Tipe Data via Pydantic     │       │
                         │        └───────────────────┬────────────────────┘       │
                         │                            │                            │
                         │         Eksekusi Deterministik                          │
                         │                            ▼                            │
                         │        ┌────────────────────────────────────────┐       │
                         │        │       FINANCIAL TOOL REGISTRY (ALU)    │       │
                         │        │ 1. query_ledger_transactions           │       │
                         │        │ 2. calculate_reconciliation_variance   │       │
                         │        │ 3. detect_duplicate_invoices           │       │
                         │        │ 4. post_ledger_adjustment (Write)      │       │
                         │        └───────────────────┬────────────────────┘       │
                         │                            │                            │
                         │         Data Observasi     │                            │
                         │         (Angka Eksak)      ▼                            │
                         └────────────────────────────┴────────────────────────────┘
                                                      │
                                          Kondisi Selesai Tercapai
                                                      ▼
                                  ┌────────────────────────────────────────┐
                                  │      VERIFIED AUDIT RECONCILIATION     │
                                  │  - Rekonsiliasi Saldo Presisi Tinggi   │
                                  │  - Deteksi Duplikasi & Selisih Kurs    │
                                  │  - Rekomendasi Jurnal Penyesuaian      │
                                  │  - Log Jejak Audit Transparan          │
                                  └────────────────────────────────────────┘
```

---

## 📁 Struktur Direktori Repositori

```text
agentic_financial_audit/
├── .gitignore                      # Mengabaikan berkas cache dan virtual environment
├── README.md                       # Dokumentasi akademik dan petunjuk operasional
├── requirements.txt                # Dependensi pustaka Python
├── config.py                       # Konfigurasi sistem dan batasan toleransi varians
├── app.py                          # Antarmuka web interaktif Streamlit
├── data/
│   └── erp_financial_transactions.csv  # Basis data transaksi buku besar & ERP
└── agent/
    ├── __init__.py
    ├── schema.py                   # Kontrak JSON Schema dan model Pydantic
    ├── tools.py                    # Financial Tool Registry deterministik
    └── engine.py                   # Mesin orkestrator kognitif dan loop audit
```

---

## 🚀 Panduan Instalasi & Eksekusi Lokal

Bagi peneliti, dosen, maupun praktisi yang ingin menjalankan dan memodifikasi sistem ini di lingkungan lokal:

### 1. Kloning Repositori
```bash
git clone https://github.com/muryanawaludin/agentic_financial_audit.git
cd agentic_financial_audit
```

### 2. Siapkan Virtual Environment (Direkomendasikan)
```bash
# Membuat virtual environment
python -m venv venv

# Aktivasi di Windows (Command Prompt):
venv\Scripts\activate

# Aktivasi di Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Aktivasi di Linux / MacOS:
source venv/bin/activate
```

### 3. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi Streamlit
```bash
streamlit run app.py
```
Aplikasi akan secara otomatis terbuka pada peramban default Anda di alamat `http://localhost:8501`.

---

## 🧪 Skenario Pengujian Audit Industri

Sistem menyediakan skenario verifikasi otomatis berdasarkan transaksi riil:

1. **Vendor VND-801 (PT Global Nusa Medika):**  
   *Kasus Seimbang Sempurna.* Total faktur tepat bernilai sama dengan penyelesaian kas masuk. Status: `FULLY_RECONCILED`.
2. **Vendor VND-802 / VND-805 (CV Rekayasa Utama / PT Tirta Sentosa):**  
   *Kasus Selisih Biaya Bank / Pembulatan.* Terdapat selisih kecil (misal Rp 750 atau Rp 2.500). Nilai di bawah ambang batas toleransi Rp 1.000 secara otonom diterbitkan jurnal penyesuaian. Status: `AUTO_ADJUSTED`.
3. **Vendor VND-803 (PT Sinar Logistik):**  
   *Kasus Anomali Pembayaran Ganda.* Alat mendeteksi nomor referensi pembayaran duplikat pada selang waktu beberapa detik. Status: `FLAGGED_FOR_HUMAN_AUDITOR`.
4. **Vendor VND-804 (PT Mandiri Mega Sarana):**  
   *Kasus Disparitas Nominal Besar.* Terdeteksi selisih Rp 500.000,00 yang melampaui batas toleransi otomatis. Agen mengeskalasikan temuan kepada auditor manusia.

---

## 📚 Referensi Akademik Terpilih

- Bubeck, S., et al. (2023). *Sparks of Artificial General Intelligence: Early experiments with GPT-4*. arXiv preprint arXiv:2303.12712.
- Gou, Z., et al. (2024). *CRITIC: Large language models can self-correct with tool-interactive critiquing*. ICLR 2024.
- Karpas, E., et al. (2022). *MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning*. arXiv preprint arXiv:2205.00445.
- Patil, S. G., et al. (2023). *Gorilla: Large language model simply connected with APIs*. arXiv preprint arXiv:2305.15334.
- Qin, Y., et al. (2023). *ToolLLM: Facilitating large language models to master 16000+ real-world APIs*. arXiv preprint arXiv:2307.16789.
- Schick, T., et al. (2023). *Toolformer: Language models can teach themselves to use tools*. NeurIPS 2023.
- Willard, B. T., & Louf, R. (2023). *Efficient guided generation for large language models with Outlines*. arXiv preprint arXiv:2307.09702.

---

## 👨‍💻 Penulis & Peneliti

**Muryan Awaludin, S.Kom., M.Kom.**  
Dosen, Peneliti Kecerdasan Buatan, dan Praktisi Konsultan Teknologi Informasi.  
- GitHub: [@muryanawaludin](https://github.com/muryanawaludin)  
- Repositori Proyek: [agentic_financial_audit](https://github.com/muryanawaludin/agentic_financial_audit.git)

---

## ⚖️ Hak Cipta & Lisensi

Hak Cipta © 2026 **Muryan Awaludin**. Seluruh hak cipta dilindungi undang-undang.

Karya ini dirancang sebagai materi referensi akademik dan implementasi industri dalam buku *Rekayasa Agentic AI*. Dilarang keras menggandakan, mendistribusikan kembali, atau mempublikasikan sebagian atau seluruh isi kode dan teks ini tanpa mencantumkan atribusi resmi kepada penulis asli.
