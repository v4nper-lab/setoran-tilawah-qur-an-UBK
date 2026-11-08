import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Aplikasi Setoran Tilawah",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# File penyimpanan lokal untuk persistensi data
DATA_FILE = "data_tilawah.json"


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return []
  return []


def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# Inisialisasi session state
if "tilawah_data" not in st.session_state:
  st.session_state.tilawah_data = load_data()

# Styling kustom (Nuansa Islami: Emerald & Gold)
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #065F46;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #4B5563;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background-color: #059669;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #047857;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Utama
st.markdown(
    '<div class="main-header">📖 Aplikasi Setoran Tilawah & Tahfidz</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Catat dan pantau progress hafalan serta'
    ' tilawah harian dengan mudah dan terstruktur.</div>',
    unsafe_allow_html=True,
)

# --- SIDEBAR: FORM TAMBAH SETORAN ---
st.sidebar.header("➕ Tambah Setoran Baru")
with st.sidebar.form("form_tilawah", clear_on_submit=True):
  nama = st.text_input("Nama Peserta / Santri")
  tanggal = st.date_input("Tanggal Setoran", value=datetime.now())
  jenis = st.selectbox(
      "Jenis Setoran",
      [
          "Ziadah (Hafalan Baru)",
          "Muroja'ah (Ulang Hafalan)",
          "Tilawah (Bukan Hafalan)",
      ],
  )
  surah_juz = st.text_input(
      "Surah / Juz / Halaman", placeholder="Contoh: Al-Baqarah 1-25"
  )
  penilaian = st.selectbox(
      "Predikat / Keterangan",
      ["Lancar", "Sangat Lancar", "Kurang Lancar", "Perlu Diulang"],
  )
  catatan_penguji = st.text_area("Catatan Penguji / Guru (Opsional)")

  submit = st.form_submit_button("Simpan Setoran")

  if submit:
    if not nama.strip() or not surah_juz.strip():
      st.sidebar.error("Nama dan keterangan Surah/Juz wajib diisi!")
    else:
      new_entry = {
          "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
          "nama": nama.strip(),
          "tanggal": tanggal.strftime("%Y-%m-%d"),
          "jenis": jenis,
          "surah_juz": surah_juz.strip(),
          "penilaian": penilaian,
          "catatan": catatan_penguji.strip(),
      }
      st.session_state.tilawah_data.insert(0, new_entry)
      save_data(st.session_state.tilawah_data)
      st.sidebar.success(f"Setoran untuk {nama} berhasil disimpan!")
      st.rerun()

# --- MAIN AREA: DASHBOARD METRICS ---
data = st.session_state.tilawah_data
total_setoran = len(data)
total_peserta = len(set(item["nama"] for item in data)) if data else 0
ziadah_count = sum(1 for item in data if "Ziadah" in item["jenis"])

col1, col2, col3 = st.columns(3)
with col1:
  st.metric(label="Total Setoran Tercatat", value=total_setoran)
with col2:
  st.metric(label="Total Peserta / Santri", value=total_peserta)
with col3:
  st.metric(label="Total Setoran Hafalan Baru", value=ziadah_count)

st.divider()

# --- RIWAYAT & TABEL DATA ---
st.subheader("📋 Riwayat Setoran Tilawah")

if not data:
  st.info(
      "Belum ada data setoran yang tercatat. Silakan gunakan form di sidebar"
      " sebelah kiri untuk menambahkan data."
  )
else:
  df = pd.DataFrame(data)

  # Filter dan Pencarian
  col_f1, col_f2 = st.columns(2)
  with col_f1:
    search_name = st.text_input("🔍 Cari berdasarkan Nama Peserta")
  with col_f2:
    filter_jenis = st.selectbox(
        "Filter Jenis Setoran", ["Semua"] + list(df["jenis"].unique())
    )

  filtered_df = df.copy()
  if search_name:
    filtered_df = filtered_df[
        filtered_df["nama"].str.contains(search_name, case=False, na=False)
    ]
  if filter_jenis != "Semua":
    filtered_df = filtered_df[filtered_df["jenis"] == filter_jenis]

  if not filtered_df.empty:
    display_df = filtered_df[
        ["tanggal", "nama", "jenis", "surah_juz", "penilaian", "catatan"]
    ].rename(
        columns={
            "tanggal": "Tanggal",
            "nama": "Nama Peserta",
            "jenis": "Jenis Setoran",
            "surah_juz": "Surah / Juz",
            "penilaian": "Predikat",
            "catatan": "Catatan",
        }
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Laporan (CSV)",
        data=csv_data,
        file_name=f"laporan_tilawah_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
    )

    st.divider()

    with st.expander("⚙️ Kelola / Hapus Data Tertentu"):
      with st.form("form_hapus"):
        selected_id = st.selectbox(
            "Pilih setoran yang ingin dihapus:",
            options=filtered_df["id"].tolist(),
            format_func=lambda x: f"{filtered_df[filtered_df['id'] == x]['tanggal'].values[0]} - {filtered_df[filtered_df['id'] == x]['nama'].values[0]} ({filtered_df[filtered_df['id'] == x]['surah_juz'].values[0]})",
        )
        btn_hapus = st.form_submit_button("Hapus Data Terpilih")
        if btn_hapus:
          st.session_state.tilawah_data = [
              item for item in st.session_state.tilawah_data if item["id"] != selected_id
          ]
          save_data(st.session_state.tilawah_data)
          st.success("Data setoran berhasil dihapus!")
          st.rerun()
  else:
    st.warning("Tidak ada data yang sesuai dengan filter pencarian.")