import base64
import json
import os
from datetime import datetime
from fpdf import FPDF
import pandas as pd
import requests
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Setoran Tilawah Al-Qur'an - Masjid UBK",
    page_icon="📖",
    layout="centered",
)

# File penyimpanan data lokal
DATA_FILE = "data_tilawah.json"

# Daftar 114 Surah lengkap dengan informasi Juz-nya
SURAHS_DATA = [
    ("Al-Fatihah", 1),
    ("Al-Baqarah", 1),
    ("Ali 'Imran", 3),
    ("An-Nisa'", 4),
    ("Al-Ma'idah", 6),
    ("Al-An'am", 7),
    ("Al-A'raf", 8),
    ("Al-Anfal", 9),
    ("At-Taubah", 10),
    ("Yunus", 11),
    ("Hud", 11),
    ("Yusuf", 12),
    ("Ar-Ra'd", 13),
    ("Ibrahim", 13),
    ("Al-Hijr", 14),
    ("An-Nahl", 14),
    ("Al-Isra'", 15),
    ("Al-Kahf", 15),
    ("Maryam", 16),
    ("Ta-Ha", 16),
    ("Al-Anbiya'", 17),
    ("Al-Hajj", 17),
    ("Al-Mu'minun", 18),
    ("An-Nur", 18),
    ("Al-Furqan", 18),
    ("Asy-Syu'ara'", 19),
    ("An-Naml", 19),
    ("Al-Qasas", 20),
    ("Al-'Ankabut", 20),
    ("Ar-Rum", 21),
    ("Luqman", 21),
    ("As-Sajdah", 21),
    ("Al-Ahzab", 21),
    ("Saba'", 22),
    ("Fatir", 22),
    ("Yasin", 22),
    ("As-Saffat", 23),
    ("Sad", 23),
    ("Az-Zumar", 23),
    ("Ghafir", 24),
    ("Fussilat", 24),
    ("Asy-Syura", 25),
    ("Az-Zukhruf", 25),
    ("Ad-Dukhan", 25),
    ("Al-Jasiyah", 25),
    ("Al-Ahqaf", 26),
    ("Muhammad", 26),
    ("Al-Fath", 26),
    ("Al-Hujurat", 26),
    ("Qaf", 26),
    ("Az-Zariyat", 26),
    ("At-Tur", 27),
    ("An-Najm", 27),
    ("Al-Qamar", 27),
    ("Ar-Rahman", 27),
    ("Al-Waqi'ah", 27),
    ("Al-Hadid", 27),
    ("Al-Mujadilah", 28),
    ("Al-Hasyr", 28),
    ("Al-Mumtahanah", 28),
    ("As-Saff", 28),
    ("Al-Jumu'ah", 28),
    ("Al-Munafiqun", 28),
    ("At-Taghabun", 28),
    ("At-Talaq", 28),
    ("At-Tahrim", 28),
    ("Al-Mulk", 29),
    ("Al-Qalam", 29),
    ("Al-Haqqah", 29),
    ("Al-Ma'arij", 29),
    ("Nuh", 29),
    ("Al-Jinn", 29),
    ("Al-Muzzammil", 29),
    ("Al-Muddassir", 29),
    ("Al-Qiyamah", 29),
    ("Al-Insan", 29),
    ("Al-Mursalat", 29),
    ("An-Naba'", 30),
    ("An-Nazi'at", 30),
    ("'Abasa", 30),
    ("At-Takwir", 30),
    ("Al-Infitar", 30),
    ("Al-Mutaffifin", 30),
    ("Al-Insyiqaq", 30),
    ("Al-Buruj", 30),
    ("At-Tariq", 30),
    ("Al-A'la", 30),
    ("Al-Ghasyiyah", 30),
    ("Al-Fajr", 30),
    ("Al-Balad", 30),
    ("Asy-Syams", 30),
    ("Al-Lail", 30),
    ("Ad-Duha", 30),
    ("Asy-Syarh", 30),
    ("At-Tin", 30),
    ("Al-'Alaq", 30),
    ("Al-Qadr", 30),
    ("Al-Bayyinah", 30),
    ("Az-Zalzalah", 30),
    ("Al-'Adiyat", 30),
    ("Al-Qari'ah", 30),
    ("At-Takasur", 30),
    ("Al-'Asr", 30),
    ("Al-Humazah", 30),
    ("Al-Fil", 30),
    ("Quraisy", 30),
    ("Al-Ma'un", 30),
    ("Al-Kausar", 30),
    ("Al-Kafirun", 30),
    ("An-Nasr", 30),
    ("Al-Lahab", 30),
    ("Al-Ikhlas", 30),
    ("Al-Falaq", 30),
    ("An-Nas", 30),
]

# Mapping untuk dropdown dan konversi nama bersih
SURAF_DISPLAY_MAP = {f"{name} (Juz {juz})": name for name, juz in SURAHS_DATA}
SURAF_OPTIONS = list(SURAF_DISPLAY_MAP.keys())

# Bobot estimasi Juz untuk sistem target 1 hari 1 juz
JUZ_WEIGHTS = {
    "Kurang dari 1 halaman": 0.02,
    "1 halaman": 0.05,
    "2 halaman": 0.10,
    "3 halaman": 0.15,
    "5 halaman": 0.25,
    "1 juz": 1.00,
    "Lebih dari 1 juz": 1.50,
}


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


if "tilawah_entries" not in st.session_state:
  st.session_state.tilawah_entries = load_data()


# Fungsi membaca gambar lokal (Masjid & Al-Quran)
def get_img_as_base64(file_path):
  if os.path.exists(file_path):
    with open(file_path, "rb") as f:
      data = f.read()
    return base64.b64encode(data).decode()
  return ""


masjid_base64 = get_img_as_base64("masjid.jpg")
if not masjid_base64:
  masjid_base64 = get_img_as_base64("masjid.png")
if not masjid_base64:
  masjid_base64 = get_img_as_base64("masjid UBK.jpg")

quran_base64 = get_img_as_base64("quran.jpg")
if not quran_base64:
  quran_base64 = get_img_as_base64("quran.png")

# HTML untuk gambar Al-Quran di sebelah kanan judul
if quran_base64:
  image_html = f'<img src="data:image/jpeg;base64,{quran_base64}" style="width: 85px; height: 115px; object-fit: cover; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3);" alt="Quran">'
else:
  image_html = '<span style="font-size: 70px;">📖</span>'

# Styling background gambar masjid dengan overlay hijau semi-transparan
if masjid_base64:
  header_bg_style = f"background: linear-gradient(135deg, rgba(6, 78, 59, 0.92) 0%, rgba(6, 95, 70, 0.88) 50%, rgba(4, 120, 87, 0.92) 100%), url('data:image/jpeg;base64,{masjid_base64}'); background-size: cover; background-position: center;"
else:
  header_bg_style = (
      "background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857"
      " 100%);"
  )


# API Jadwal Sholat (Rancaekek, Kab. Bandung)
@st.cache_data(ttl=1800)
def get_prayer_times():
  try:
    lat = -6.9603
    lon = 107.7675
    url = f"https://api.aladhan.com/v1/timings/today?latitude={lat}&longitude={lon}&method=20"
    res = requests.get(url, timeout=5)
    if res.status_code == 200:
      data = res.json()
      return data["data"]["timings"], data["data"]["date"]["readable"]
  except:
    return None, None
  return None, None


timings, readable_date = get_prayer_times()


# Kelas Generator PDF Laporan Rekapitulasi
class PDFReport(FPDF):

  def header(self):
    self.set_font("helvetica", "B", 13)
    self.cell(
        0, 7, "MASJID JAMI' UMAR BIN KHOTTOB - RANCAEKEK", 0, 1, "C"
    )
    self.set_font("helvetica", "", 10)
    self.cell(
        0,
        5,
        "Laporan Rekapitulasi Progress Setoran Tilawah (Target 1 Hari 1 Juz)",
        0,
        1,
        "C",
    )
    self.set_font("helvetica", "I", 8)
    self.cell(
        0,
        5,
        f"Periode Cetak: {datetime.now().strftime('%d %B %Y')}",
        0,
        1,
        "C",
    )
    self.ln(4)
    self.set_draw_color(6, 78, 59)
    self.set_line_width(0.8)
    self.line(10, self.get_y(), 200, self.get_y())
    self.ln(6)

  def footer(self):
    self.set_y(-15)
    self.set_font("helvetica", "I", 8)
    self.set_text_color(100, 100, 100)
    self.cell(
        0,
        10,
        f"Program Cinta Al-Qur'an UBK © 2026 | Halaman {self.page_no()}",
        0,
        0,
        "C",
    )


def generate_pdf(rekap_df):
  pdf = PDFReport()
  pdf.add_page()
  pdf.set_auto_page_break(auto=True, margin=15)

  pdf.set_font("helvetica", "B", 10)
  pdf.set_fill_color(6, 78, 59)
  pdf.set_text_color(255, 255, 255)

  pdf.cell(12, 8, "No", 1, 0, "C", True)
  pdf.cell(70, 8, "Nama Jamaah", 1, 0, "L", True)
  pdf.cell(30, 8, "Setoran", 1, 0, "C", True)
  pdf.cell(35, 8, "Est. Juz", 1, 0, "C", True)
  pdf.cell(43, 8, "Pencapaian", 1, 1, "C", True)

  pdf.set_font("helvetica", "", 10)
  pdf.set_text_color(0, 0, 0)

  for idx, row in rekap_df.iterrows():
    fill = idx % 2 == 1
    if fill:
      pdf.set_fill_color(240, 253, 244)
    else:
      pdf.set_fill_color(255, 255, 255)

    pdf.cell(12, 7, str(idx + 1), 1, 0, "C", True)
    pdf.cell(70, 7, str(row["nama"]), 1, 0, "L", True)
    pdf.cell(30, 7, str(row["Jumlah_Setoran"]) + "x", 1, 0, "C", True)
    pdf.cell(35, 7, f"{row['Total_Juz']:.2f} Juz", 1, 0, "C", True)
    pdf.cell(43, 7, f"{row['Persen']}%", 1, 1, "C", True)

  pdf.ln(10)
  pdf.set_font("helvetica", "I", 9)
  pdf.set_text_color(50, 50, 50)
  pdf.multi_cell(
      0,
      5,
      (
          '"Sebaik-baik kalian adalah orang yang mempelajari Al-Qur\'an dan'
          ' mengajarkannya." (HR. Bukhari)\nTerus istiqomah membersamai'
          " Al-Qur'an setiap hari demi meraih syafaat di hari kiamat."
      ),
      0,
      "C",
  )

  return bytes(pdf.output())


# 1. Styling CSS dengan Background Masjid di Header
st.markdown(
    f"""
    <style>
    .header-card {{
        {header_bg_style}
        color: white;
        padding: 34px 28px;
        border-radius: 24px;
        box-shadow: 0 12px 30px -5px rgba(6, 95, 70, 0.4);
        margin-bottom: 20px;
    }
    .brand-tag {{ 
        font-size: 13px; 
        letter-spacing: 0.12em; 
        text-transform: uppercase; 
        font-weight: 700; 
        opacity: 0.95; 
        background: rgba(255,255,255,0.22); 
        padding: 5px 14px; 
        border-radius: 20px; 
        display: inline-block;
        margin-bottom: 10px; 
    }}
    .hero-title {{ 
        font-size: 34px; 
        font-weight: 800; 
        line-height: 1.15; 
        margin: 6px 0 10px 0; 
        font-family: 'Cinzel', 'Trajan Pro', 'Georgia', serif;
        text-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }}
    .hero-sub {{ 
        font-size: 16px; 
        opacity: 0.95; 
        font-weight: 500; 
        letter-spacing: 0.02em;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }}
    .prayer-box {{
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 14px 18px;
        border-radius: 16px;
        margin-bottom: 20px;
    }}
    .daily-box {{
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fde68a;
        padding: 16px 20px;
        border-radius: 16px;
        margin-bottom: 20px;
        color: #78350f;
    }}
    .stButton>button {{
        background: #059669;
        color: white;
        font-weight: 700;
        border-radius: 12px;
        height: 50px;
        border: none;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.2);
    }}
    .stButton>button:hover {{
        background: #047857;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. Banner Header Utama
st.markdown(
    f"""
    <div class="header-card">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <div class="brand-tag">PROGRAM CINTA AL-QUR'AN</div>
                <div class="hero-title">Setoran Tilawah<br>Al-Qur'an</div>
                <div class="hero-sub">Masjid Jami' Umar Bin Khottob</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.2); padding: 10px; border-radius: 16px; box-shadow: inset 0 2px 6px rgba(0,0,0,0.2); display: flex; align-items: center; justify-content: center;">
                {image_html}
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Widget Jadwal Sholat Rancaekek & Kab. Bandung
if timings:
  st.markdown(
      f"""
    <div class="prayer-box">
        <div style="font-size: 13px; font-weight: 700; color: #166534; margin-bottom: 6px; display: flex; justify-content: space-between;">
            <span>📍 Jadwal Sholat Hari Ini (Rancaekek & Kab. Bandung)</span>
            <span style="font-weight: 400; opacity: 0.8;">{readable_date}</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; text-align: center; font-size: 13px;">
            <div style="background: white; padding: 6px; border-radius: 8px; border: 1px solid #dcfce7;"><b>Subuh</b><br>{timings.get('Fajr', '-')}</div>
            <div style="background: white; padding: 6px; border-radius: 8px; border: 1px solid #dcfce7;"><b>Dzuhur</b><br>{timings.get('Dhuhr', '-')}</div>
            <div style="background: white; padding: 6px; border-radius: 8px; border: 1px solid #dcfce7;"><b>Ashar</b><br>{timings.get('Asr', '-')}</div>
            <div style="background: white; padding: 6px; border-radius: 8px; border: 1px solid #dcfce7;"><b>Maghrib</b><br>{timings.get('Maghrib', '-')}</div>
            <div style="background: white; padding: 6px; border-radius: 8px; border: 1px solid #dcfce7;"><b>Isya</b><br>{timings.get('Isha', '-')}</div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

# Motivasi Harian
DAILY_UPDATES = [
    (
        "💡 Motivasi Hari Ini",
        (
            "\"Sebaik-baik kalian adalah orang yang mempelajari Al-Qur'an dan"
            ' mengajarkannya.\" (HR. Bukhari)'
        ),
    ),
    (
        "✨ Keutamaan Tilawah",
        (
            "\"Bacalah Al-Qur'an, karena ia akan datang pada hari kiamat"
            " sebagai syafaat bagi pembacanya.\" (HR. Muslim)"
        ),
    ),
    (
        "Semangat Para Pejuang Tilawah Qur'an",
        (
            "\"Orang yang mahir membaca Al-Qur'an bersama para malaikat yang"
            ' mulia lagi taat...\" (HR. Muslim)'
        ),
    ),
    (
        "🌿 Tadabbur Harian",
        (
            "\"Dan bacalah Al-Qur'an dengan tartil (perlahan-lahan dan"
            ' jelas).\" (QS. Al-Muzzammil: 4)'
        ),
    ),
    (
        "💫 Cahaya Rumah",
        (
            "\"Jangan jadikan rumah kalian seperti kuburan. Sesungguhnya"
            " setan lari dari rumah yang dibacakan di dalamnya surat Al-Baqarah."
            '" (HR. Muslim)'
        ),
    ),
]

day_index = datetime.now().timetuple().tm_yday % len(DAILY_UPDATES)
update_title, update_text = DAILY_UPDATES[day_index]

st.markdown(
    f"""
<div class="daily-box">
    <div style="font-weight: 700; font-size: 14px; margin-bottom: 4px;">{update_title}</div>
    <div style="font-size: 14px; line-height: 1.4;"><i>{update_text}</i></div>
</div>
""",
    unsafe_allow_html=True,
)

# Tab Menu Utama
tab_jamaah, tab_pengurus = st.tabs(
    ["👥 Jamaah (Input Setoran)", "⚙️ Pengurus (Rekap & Grafik)"]
)

with tab_jamaah:
  st.subheader("Form Setoran Tilawah Harian")

  with st.form("form_setoran_modern", clear_on_submit=True):
    nama = st.text_input(
        "Nama Jamaah", placeholder="Contoh: Ahmad Hidayat"
    )
    tanggal = st.date_input("Tanggal Membaca", value=datetime.now())

    # Dropdown surat dengan informasi Juz
    selected_surat_display = st.selectbox(
        "Surat yang Dibaca (Disertai Info Juz)", ["Pilih Nama Surat"] + SURAF_OPTIONS
    )

    col1, col2 = st.columns(2)
    with col1:
      awal = st.number_input("Ayat Mulai", min_value=1, step=1, value=1)
    with col2:
      akhir = st.number_input("Ayat Sampai", min_value=1, step=1, value=7)

    jumlah = st.selectbox(
        "Jumlah Bacaan",
        [
            "Pilih Jumlah",
            "Kurang dari 1 halaman",
            "1 halaman",
            "2 halaman",
            "3 halaman",
            "5 halaman",
            "1 juz",
            "Lebih dari 1 juz",
        ],
    )
    catatan = st.text_input(
        "Catatan (Opsional)", placeholder="Contoh: Dibaca setelah sholat Subuh"
    )

    submitted = st.form_submit_button("🚀 SIMPAN SETORAN SEKARANG")

    if submitted:
      surat_clean = (
          SURAF_DISPLAY_MAP.get(selected_surat_display, "")
          if selected_surat_display != "Pilih Nama Surat"
          else ""
      )
      if (
          not nama.strip()
          or selected_surat_display == "Pilih Nama Surat"
          or jumlah == "Pilih Jumlah"
          or akhir < awal
      ):
        st.error(
            "Mohon lengkapi Nama, Surat dengan Juz, Rentang Ayat yang valid, dan"
            " Jumlah Bacaan dengan benar."
        )
      else:
        new_entry = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "nama": nama.strip(),
            "tanggal": tanggal.strftime("%Y-%m-%d"),
            "surat": surat_clean,
            "awal": int(awal),
            "akhir": int(akhir),
            "jumlah": jumlah,
            "catatan": catatan.strip(),
        }
        st.session_state.tilawah_entries.insert(0, new_entry)
        save_data(st.session_state.tilawah_entries)
        st.success(
            "Alhamdulillah, setoran berhasil disimpan! Barakallahu fiikum."
        )
        st.session_state["last_nama"] = nama.strip()
        st.rerun()

  st.divider()

  # Riwayat Setoran Pribadi
  st.subheader("📋 Riwayat Setoran Saya")
  filter_nama = st.text_input(
      "Ketik nama Anda untuk melihat riwayat setoran",
      value=st.session_state.get("last_nama", ""),
      key="filter_nama_input",
  )

  if not filter_nama.strip():
    st.info("Ketik nama Anda di atas untuk menampilkan riwayat setoran pribadi.")
  else:
    filtered = [
        e
        for e in st.session_state.tilawah_entries
        if e["nama"].lower() == filter_nama.strip().lower()
    ]
    if not filtered:
      st.warning("Belum ada data setoran ditemukan dengan nama tersebut.")
    else:
      total_pribadi = len(filtered)
      st.success(
          f"✨ **{filter_nama.strip()}** telah mencatatkan **{total_pribadi}x**"
          " setoran tilawah/hafalan."
      )

      for e in filtered:
        catatan_str = f" · Catatan: {e['catatan']}" if e["catatan"] else ""
        st.markdown(
            f"""
            <div style="border: 1px solid #dce8df; padding: 14px; border-radius: 12px; margin-bottom: 10px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
                <strong>{e['nama']} — Surat {e['surat']}</strong><br>
                <span style="font-size: 13px; color: #62736a;">📅 {e['tanggal']} &nbsp;|&nbsp; Ayat {e['awal']}–{e['akhir']} &nbsp;|&nbsp; 📖 {e['jumlah']}{catatan_str}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_pengurus:
  st.subheader("🔐 Panel Pengurus Masjid")
  st.markdown(
      '<p style="font-size: 13px; color: #62736a;">Masukkan PIN'
      " pengurus untuk membuka rekapitulasi data dan grafik.</p>",
      unsafe_allow_html=True,
  )

  admin_pin_rahasia = st.secrets.get("ADMIN_PIN", "1234")

  # Input PIN dikembalikan menggunakan type="password" (titik-titik / tersembunyi)
  pin = st.text_input(
      "PIN Pengurus", type="password", placeholder="Masukkan PIN 1234"
  )

  if st.button("Buka Panel Pengurus"):
    if pin == admin_pin_rahasia:
      st.session_state["admin_logged"] = True
    else:
      st.error("PIN salah!")
      st.session_state["admin_logged"] = False

  if st.session_state.get("admin_logged", False):
    st.success("Akses panel pengurus diberikan.")
    entries = st.session_state.tilawah_entries

    total_setoran = len(entries)
    total_jamaah = len(set(e["nama"].lower() for e in entries))

    col1, col2 = st.columns(2)
    with col1:
      st.metric(label="Total Seluruh Setoran", value=total_setoran)
    with col2:
      st.metric(label="Total Partisipasi Jamaah", value=total_jamaah)

    if entries:
      df = pd.DataFrame(entries)

      st.markdown("---")
      st.markdown("### 📈 Grafik Statistik Setoran per Jamaah")
      chart_data = df["nama"].value_counts().reset_index()
      chart_data.columns = ["Nama Jamaah", "Jumlah Setoran"]
      chart_data = chart_data.set_index("Nama Jamaah")
      st.bar_chart(chart_data)

      st.markdown("### 📊 Rekapitulasi & Progress (Target 1 Hari 1 Juz)")

      rekap_list = []
      for nama_j, group in df.groupby("nama"):
        jml_setoran = len(group)
        last_dt = group["tanggal"].max()
        first_dt = group["tanggal"].min()

        total_juz = sum(
            group["jumlah"].map(JUZ_WEIGHTS).fillna(0.1)
        )
        days_active = max(
            1,
            (datetime.now().date() - pd.to_datetime(first_dt).date()).days + 1,
        )
        target_juz = float(days_active * 1.0)

        persen = min(int((total_juz / target_juz) * 100), 100)
        rekap_list.append({
            "nama": nama_j,
            "Jumlah_Setoran": jml_setoran,
            "Total_Juz": total_juz,
            "Setoran_Terakhir": last_dt,
            "Persen": persen,
        })

      rekap_jamaah = pd.DataFrame(rekap_list)

      for idx, row in rekap_jamaah.iterrows():
        st.markdown(
            f"**{row['nama']}** — {row['Jumlah_Setoran']} setoran (Est. "
            f"**{row['Total_Juz']:.2f} Juz** dari Target 1 Hari 1 Juz) —"
            f" Pencapaian: **{row['Persen']}%**"
        )
        st.progress(row["Persen"] / 100.0)

      with st.expander("📋 Lihat Tabel Rekap Detail"):
        st.dataframe(rekap_jamaah, use_container_width=True, hide_index=True)

      with st.expander("🔍 Lihat Detail Riwayat Spesifik Per Jamaah"):
        pilih_jamaah = st.selectbox(
            "Pilih Nama Jamaah", sorted(df["nama"].unique())
        )
        detail_jamaah = df[df["nama"] == pilih_jamaah]
        for idx, row in detail_jamaah.iterrows():
          catatan_str = f" · Catatan: {row['catatan']}" if row["catatan"] else ""
          st.markdown(
              f"- 📅 **{row['tanggal']}** | Surat **{row['surat']}** (Ayat"
              f" {row['awal']}–{row['akhir']}) - *{row['jumlah']}*{catatan_str}"
          )

      st.divider()

      # Tombol Download Laporan PDF untuk Print Out / Share Grup WA
      st.markdown("### 🖨️ Cetak & Unduh Laporan PDF")
      st.markdown(
          '<p style="font-size: 13px; color: #62736a;">Unduh laporan'
          " rekapitulasi progress jamaah berformat PDF untuk dicetak atau"
          " dibagikan mingguan/harian ke grup WhatsApp guna memotivasi"
          " jamaah.</p>",
          unsafe_allow_html=True,
      )

      pdf_bytes = generate_pdf(rekap_jamaah)
      st.download_button(
          label="📄 Unduh Laporan Rekap PDF",
          data=pdf_bytes,
          file_name=(
              f"Laporan_Tilawah_UBK_{datetime.now().strftime('%Y-%m-%d')}.pdf"
          ),
          mime="application/pdf",
      )

      st.markdown("---")

      # Tombol Ekspor CSV
      csv = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="📥 Unduh Rekap Laporan Excel (CSV)",
          data=csv,
          file_name=f"rekap_tilawah_{datetime.now().strftime('%Y-%m-%d')}.csv",
          mime="text/csv",
      )

      # Tombol Hapus Data
      if st.button("🗑️ Hapus Seluruh Data Di Perangkat Ini", type="primary"):
        st.session_state.tilawah_entries = []
        save_data([])
        st.success("Semua data berhasil dibersihkan.")
        st.rerun()

      st.markdown("### 📁 Daftar Log Seluruh Setoran Masuk")
      for e in entries:
        catatan_str = f" · Catatan: {e['catatan']}" if e['catatan'] else ""
        st.markdown(
            f"""
            <div style="border: 1px solid #dce8df; padding: 12px; border-radius: 10px; margin-bottom: 8px; background: white;">
                <strong>{e['nama']} — Surat {e['surat']}</strong><br>
                <span style="font-size: 13px; color: #62736a;">📅 {e['tanggal']} · Ayat {e['awal']}–{e['akhir']} · {e['jumlah']}{catatan_str}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
      st.info("Belum ada data setoran yang masuk.")

# Footer Estetik
st.markdown(
    """
    <div style="text-align: center; color: #62736a; font-size: 13px; margin-top: 40px; padding-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
        ✨ <i>Semoga Allah menjadikan Al-Qur'an sebagai cahaya dalam kehidupan kita sehari-hari.</i> ✨<br>
        <b>Masjid Jami' Umar Bin Khottob © 2026</b>
    </div>
    """,
    unsafe_allow_html=True,
)
