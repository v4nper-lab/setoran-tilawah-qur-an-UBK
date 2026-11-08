import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Setoran Tilawah Al-Qur'an", page_icon="📖", layout="centered"
)

# File penyimpanan data lokal
DATA_FILE = "data_tilawah.json"

# Daftar 114 Surah sesuai standar HTML
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

# Styling header dan nuansa warna hijau khas Masjid Umar Bin Khottob
st.markdown(
    """
    <style>
    .header-box {
        background: linear-gradient(135deg, #10472e, #1e754b);
        color: white;
        padding: 24px 18px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    .brand { font-size: 13px; opacity: 0.9; font-weight: 700; letter-spacing: 0.08em; }
    .hero { font-size: 26px; font-weight: 800; line-height: 1.15; margin: 6px 0; }
    .sub { font-size: 15px; opacity: 0.9; }
    .notice {
        background: #fff8e6;
        border: 1px solid #f0dfaa;
        padding: 12px;
        border-radius: 12px;
        font-size: 14px;
        color: #554400;
        margin-bottom: 16px;
    }
    </style>
    <div class="header-box">
        <div class="brand">PROGRAM CINTA AL-QUR'AN</div>
        <div class="hero">Setoran Tilawah Al-Qur'an</div>
        <div class="sub">Masjid Jami' Umar Bin Khottob</div>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="notice"><b>Petunjuk:</b> Isi nama sesuai nama yang biasa'
    " digunakan di masjid. Pilih surat dan ayat yang dibaca, lalu tekan tombol"
    " <b>SIMPAN SETORAN</b>.</div>",
    unsafe_allow_html=True,
)

# Tab menu Utama: Jamaah & Pengurus
tab_jamaah, tab_pengurus = st.tabs(["Jamaah", "Pengurus"])

with tab_jamaah:
  st.subheader("Form Setoran Tilawah")

  with st.form("form_setoran", clear_on_submit=True):
    nama = st.text_input(
        "Nama jamaah", placeholder="Contoh: Ahmad Hidayat"
    )
    tanggal = st.date_input("Tanggal membaca", value=datetime.now())
    surat = st.selectbox(
        "Surat yang dibaca", ["Pilih nama surat"] + SURAHS
    )

    col1, col2 = st.columns(2)
    with col1:
      awal = st.number_input("Ayat mulai", min_value=1, step=1, value=1)
    with col2:
      akhir = st.number_input("Ayat sampai", min_value=1, step=1, value=7)

    jumlah = st.selectbox(
        "Jumlah bacaan",
        [
            "Pilih jumlah",
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
        "Catatan (boleh dikosongkan)",
        placeholder="Contoh: dibaca setelah Subuh",
    )

    submitted = st.form_submit_button("SIMPAN SETORAN")

    if submitted:
      if (
          not nama.strip()
          or surat == "Pilih nama surat"
          or jumlah == "Pilih jumlah"
          or akhir < awal
      ):
        st.error(
            "Mohon lengkapi nama, pilih surat yang valid, rentang ayat yang"
            " benar, dan jumlah bacaan."
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
            "Alhamdulillah, setoran tersimpan di perangkat ini."
        )
        st.session_state["last_nama"] = nama.strip()
        st.rerun()

  st.divider()

  # Bagian Riwayat Setoran Saya
  st.subheader("Riwayat Setoran Saya")
  filter_nama = st.text_input(
      "Masukkan nama untuk melihat riwayat sendiri",
      value=st.session_state.get("last_nama", ""),
      key="filter_nama_input",
  )

  if not filter_nama.strip():
    st.info("Riwayat setoran akan tampil di sini. Masukkan nama jamaah.")
  else:
    filtered = [
        e
        for e in st.session_state.tilawah_entries
        if e["nama"].lower() == filter_nama.strip().lower()
    ]
    if not filtered:
      st.warning("Belum ada setoran dengan nama tersebut.")
    else:
      for e in filtered:
        catatan_str = f" · Catatan: {e['catatan']}" if e["catatan"] else ""
        st.markdown(
            f"""
            <div style="border: 1px solid #dce8df; padding: 12px; border-radius: 10px; margin-bottom: 8px; background: white;">
                <strong>{e['nama']} — {e['surat']}</strong><br>
                <span style="font-size: 14px; color: #62736a;">{e['tanggal']} · Ayat {e['awal']}–{e['akhir']} · {e['jumlah']}{catatan_str}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_pengurus:
  st.subheader("Halaman Pengurus")
  st.markdown(
      '<p style="font-size: 14px; color: #62736a;">Untuk prototipe ini,'
      " masukkan PIN contoh <b>1234</b>.</p>",
      unsafe_allow_html=True,
  )

  pin = st.text_input("PIN pengurus", type="password")
  if st.button("BUKA REKAP"):
    if pin == "1234":
      st.session_state["admin_logged"] = True
    else:
      st.error("PIN salah. Untuk demo, gunakan 1234.")
      st.session_state["admin_logged"] = False

  if st.session_state.get("admin_logged", False):
    st.success("Login berhasil!")
    entries = st.session_state.tilawah_entries

    total_setoran = len(entries)
    total_jamaah = len(set(e["nama"].lower() for e in entries))

    c1, c2 = st.columns(2)
    with c1:
      st.metric("Total setoran", total_setoran)
    with c2:
      st.metric("Nama jamaah", total_jamaah)

    if entries:
      df = pd.DataFrame(entries)
      csv = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="UNDUH REKAP EXCEL (CSV)",
          data=csv,
          file_name="rekap-setoran-tilawah.csv",
          mime="text/csv",
      )

      if st.button("Hapus seluruh data di perangkat ini", type="primary"):
        st.session_state.tilawah_entries = []
        save_data([])
        st.success("Seluruh data berhasil dihapus.")
        st.rerun()

      st.markdown("### Daftar Seluruh Setoran")
      for e in entries:
        catatan_str = f" · Catatan: {e['catatan']}" if e["catatan"] else ""
        st.markdown(
            f"""
            <div style="border: 1px solid #dce8df; padding: 12px; border-radius: 10px; margin-bottom: 8px; background: white;">
                <strong>{e['nama']} — {e['surat']}</strong><br>
                <span style="font-size: 14px; color: #62736a;">{e['tanggal']} · Ayat {e['awal']}–{e['akhir']} · {e['jumlah']}{catatan_str}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
      st.info("Belum ada setoran.")

st.markdown(
    '<div class="notice" style="margin-top: 30px;"><b>Catatan penting:</b> Ini'
    " prototipe aplikasi Masjid Jami' Umar Bin Khottob. Data tersimpan di"
    " perangkat server aplikasi.</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="text-align: center; color: #62736a; font-size: 13px; margin-top'
    ': 20px;">Semoga Allah menjadikan Al-Qur\'an cahaya dalam kehidupan kita.'
    " Aamiin.</div>",
    unsafe_allow_html=True,
)