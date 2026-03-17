# 🚀 Bot Aktivitas IWK (GitHub Commit Summarizer)

Bot otomatis yang mengambil pesan komit GitHub Anda dalam 12 jam terakhir, merangkumnya menggunakan **Google Gemini AI**, dan mengirimkan laporannya ke **Telegram**.

## 🛠 Fitur
- **Otomatis**: Berjalan setiap hari pukul 18:00 WIB via GitHub Actions.
- **Cerdas**: Merangkum komit teknis menjadi bahasa profesional yang mudah dibaca.
- **Multi-Repo**: Dapat memantau banyak repositori sekaligus.
- **Serverless**: Berjalan sepenuhnya di infrastruktur GitHub Actions (Gratis).

## 🔑 Kebutuhan API Key
Anda perlu menyiapkan 4 kredensial berikut:

1.  **GitHub PAT (Personal Access Token)**:
    - Buat di: [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens).
    - Pastikan memiliki izin `repo` (atau `Contents: Read`).
2.  **Gemini API Key**:
    - Dapatkan di [Google AI Studio](https://aistudio.google.com/).
3.  **Telegram Bot Token**:
    - Dapatkan dari [@BotFather](https://t.me/botfather) di Telegram.
4.  **Telegram Chat ID**:
    - Dapatkan ID chat Anda melalui [@userinfobot](https://t.me/userinfobot).

---

## 💻 Instalasi Lokal (Untuk Testing)

Gunakan langkah ini jika Anda ingin mencoba bot di komputer Anda sebelum dideploy ke GitHub.

1.  **Clone Repositori**:
    ```bash
    git clone https://github.com/username/bot-aktivitas-iwk.git
    cd bot-aktivitas-iwk
    ```
2.  **Instalasi Library**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Konfigurasi Environment**:
    - Salin file `.env.example` menjadi `.env`.
    - Buka file `.env` dan isi dengan API Key Anda.
4.  **Konfigurasi Repositori**:
    - Buka `main.py` dan ubah daftar `REPOSITORIES` sesuai keinginan.
5.  **Jalankan**:
    ```bash
    python main.py
    ```

---

## 🚀 Deploy ke GitHub (GitHub Actions)

Gunakan langkah ini agar bot berjalan otomatis setiap hari tanpa perlu menyalakan komputer Anda.

### 1. Push ke GitHub
Setelah Anda mengedit `main.py` (untuk daftar repositori), unggah kode Anda ke repositori GitHub:
```bash
git add .
git commit -m "Setup bot harian"
git push origin main
```

### 2. Konfigurasi GitHub Secrets
Agar aman, API Key tidak disimpan di dalam kode, melainkan di fitur **Secrets** GitHub:
1. Masuk ke repositori Anda di GitHub.
2. Klik **Settings** > **Secrets and variables** > **Actions**.
3. Klik **New repository secret** untuk setiap variabel berikut:
   - `GITHUB_PAT` (Wajib - Izin: `repo`)
   - `GEMINI_API_KEY` (Wajib)
   - `TELEGRAM_BOT_TOKEN` (Wajib)
   - `TELEGRAM_CHAT_ID` (Wajib)
   - `GITHUB_USERNAME` (Opsional - Isi jika Anda ingin mengambil komit dari akun/organisasi lain)

> **💡 Tips Organisasi:** Gunakan format `"nama-organisasi/nama-repo"` di dalam `main.py` untuk memantau repositori di luar akun pribadi Anda.

### 3. Cara Menjalankan Manual (Testing di GitHub)
Bot ini diatur untuk berjalan otomatis setiap pukul **18:00 WIB**. Namun, Anda bisa menjalankannya kapan saja untuk tes:
1. Klik tab **Actions** di bagian atas repositori GitHub Anda.
2. Klik **Daily Commit Summary** di bilah sisi kiri.
3. Klik tombol **Run workflow** > **Run workflow**.
4. Tunggu beberapa saat, dan cek bot Telegram Anda!

---

## 📂 Struktur Proyek
- `main.py`: Logika utama ekstraksi, perangkuman, dan pengiriman.
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan.
- `.github/workflows/daily-summary.yml`: Konfigurasi jadwal otomatis.
- `.env.example`: Template konfigurasi environment.
- `.gitignore`: Memastikan file rahasia tidak terunggah ke publik.

---
Dibuat dengan ❤️ untuk efisiensi laporan harian.
