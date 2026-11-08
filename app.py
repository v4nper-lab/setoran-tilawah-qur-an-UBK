import json
import os
from datetime import datetime
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

# Daftar 114 Surah
SURAHS = [
    "Al-Fatihah",
    "Al-Baqarah",
    "Ali 'Imran",
    "An-Nisa'",
    "Al-Ma'idah",
    "Al-An'am",
    "Al-A'raf",
    "Al-Anfal",
    "At-Taubah",
    "Yunus",
    "Hud",
    "Yusuf",
    "Ar-Ra'd",
    "Ibrahim",
    "Al-Hijr",
    "An-Nahl",
    "Al-Isra'",
    "Al-Kahf",
    "Maryam",
    "Ta-Ha",
    "Al-Anbiya'",
    "Al-Hajj",
    "Al-Mu'minun",
    "An-Nur",
    "Al-Furqan",
    "Asy-Syu'ara'",
    "An-Naml",
    "Al-Qasas",
    "Al-'Ankabut",
    "Ar-Rum",
    "Luqman",
    "As-Sajdah",
    "Al-Ahzab",
    "Saba'",
    "Fatir",
    "Yasin",
    "As-Saffat",
    "Sad",
    "Az-Zumar",
    "Ghafir",
    "Fussilat",
    "Asy-Syura",
    "Az-Zukhruf",
    "Ad-Dukhan",
    "Al-Jasiyah",
    "Al-Ahqaf",
    "Muhammad",
    "Al-Fath",
    "Al-Hujurat",
    "Qaf",
    "Az-Zariyat",
    "At-Tur",
    "An-Najm",
    "Al-Qamar",
    "Ar-Rahman",
    "Al-Waqi'ah",
    "Al-Hadid",
    "Al-Mujadilah",
    "Al-Hasyr",
    "Al-Mumtahanah",
    "As-Saff",
    "Al-Jumu'ah",
    "Al-Munafiqun",
    "At-Taghabun",
    "At-Talaq",
    "At-Tahrim",
    "Al-Mulk",
    "Al-Qalam",
    "Al-Haqqah",
    "Al-Ma'arij",
    "Nuh",
    "Al-Jinn",
    "Al-Muzzammil",
    "Al-Muddassir",
    "Al-Qiyamah",
    "Al-Insan",
    "Al-Mursalat",
    "An-Naba'",
    "An-Nazi'at",
    "'Abasa",
    "At-Takwir",
    "Al-Infitar",
    "Al-Mutaffifin",
    "Al-Insyiqaq",
    "Al-Buruj",
    "At-Tariq",
    "Al-A'la",
    "Al-Ghasyiyah",
    "Al-Fajr",
    "Al-Balad",
    "Asy-Syams",
    "Al-Lail",
    "Ad-Duha",
    "Asy-Syarh",
    "At-Tin",
    "Al-'Alaq",
    "Al-Qadr",
    "Al-Bayyinah",
    "Az-Zalzalah",
    "Al-'Adiyat",
    "Al-Qari'ah",
    "At-Takasur",
    "Al-'Asr",
    "Al-Humazah",
    "Al-Fil",
    "Quraisy",
    "Al-Ma'un",
    "Al-Kausar",
    "Al-Kafirun",
    "An-Nasr",
    "Al-Lahab",
    "Al-Ikhlas",
    "Al-Falaq",
    "An-Nas",
]


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


# API Pengambilan Jadwal Sholat Otomatis (Rancaekek, Kab. Bandung)
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

# Styling Modern Glassmorphism & Emerald Theme dengan Judul Baru
st.markdown(
    """
    <style>
    .header-card {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
        color: white;
        padding: 28px 24px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(6, 95, 70, 0.3);
        margin-bottom: 20px;
    }
    .brand-tag { font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 700; opacity: 0.9; margin-bottom: 6px;}
    .hero-title { font-size: 28px; font-weight: 800; line-height: 1.15; margin: 4px 0 8px 0; }
    .hero-sub { font-size: 15px; opacity: 0.9; font-weight: 400; }
    .prayer-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 14px 18px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    .daily-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fde68a;
        padding: 16px 20px;
        border-radius: 16px;
        margin-bottom: 20px;
        color: #78350f;
    }
    .stButton>button {
        background: #059669;
        color: white;
        font-weight: 700;
        border-radius: 12px;
        height: 50px;
        border: none;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.2);
    }
    .stButton>button:hover {
        background: #047857;
    }
    </style>
    <div class="header-card">
        <div class="brand-tag">PROGRAM CINTA AL-QUR'AN</div>
        <div class="hero-title">Setoran Tilawah<br>Al-Qur'an</div>
        <div class="hero-sub">Masjid Jami' Umar Bin Khottob</div>
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

# Motivasi Harian Otomatis
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
        "🌟 Semangat Tahfidz",
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
    <div style="font-weight: 700; font-size: 14px; margin-bottom: 4px;">{update_title} (Update Otomatis Harian)</div>
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
    surat = st.selectbox(
        "Surat yang Dibaca", ["Pilih Nama Surat"] + SURAHS
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
      if (
          not nama.strip()
          or surat == "Pilih Nama Surat"
          or jumlah == "Pilih Jumlah"
          or akhir < awal
      ):
        st.error(
            "Mohon lengkapi Nama, Surat, Rentang Ayat yang valid, dan Jumlah"
            " Bacaan dengan benar."
        )
      else:
        new_entry = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "nama": nama.strip(),
            "tanggal": tanggal.strftime("%Y-%m-%d"),
            "surat": surat,
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

  pin = st.text_input("PIN Pengurus", type="password")
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

      st.markdown("### 📊 Rekapitulasi & Persentase Progress Jamaah")
      rekap_jamaah = (
          df.groupby("nama")
          .agg(
              Jumlah_Setoran=("surat", "count"),
              Setoran_Terakhir=("tanggal", "max"),
          )
          .reset_index()
      )

      target_ideal = 20
      for idx, row in rekap_jamaah.iterrows():
        nama_j = row["nama"]
        jml = row["Jumlah_Setoran"]
        last_dt = row["Setoran_Terakhir"]
        persen = min(int((jml / target_ideal) * 100), 100)

        st.markdown(
            f"**{nama_j}** — {jml} setoran *(Terakhir: {last_dt})* — Target"
            f" Tercapai: {persen}%"
        )
        st.progress(persen / 100.0)

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

      csv = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="📥 Unduh Rekap Laporan Excel (CSV)",
          data=csv,
          file_name=f"rekap_tilawah_{datetime.now().strftime('%Y-%m-%d')}.csv",
          mime="text/csv",
      )

      if st.button("🗑️ Hapus Seluruh Data Di Perangkat Ini", type="primary"):
        st.session_state.tilawah_entries = []
        save_data([])
        st.success("Semua data berhasil dibersihkan.")
        st.rerun()

      st.markdown("### 📁 Daftar Log Seluruh Setoran Masuk")
      for e in entries:
        catatan_str = f" · Catatan: {e['catatan']}" if e["catatan"] else ""
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
