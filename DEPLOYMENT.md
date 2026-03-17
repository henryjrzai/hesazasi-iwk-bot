# 🚀 Panduan Deployment ke GitHub Actions

Ikuti panduan ini untuk membuat bot Anda berjalan otomatis setiap hari pukul 18:00 WIB menggunakan infrastruktur GitHub (gratis).

---

## 🏗 Langkah 1: Persiapan Kode
Sebelum diunggah, pastikan Anda telah menentukan repositori mana saja yang ingin dipantau.

1. Buka file `main.py`.
2. Cari variabel `REPOSITORIES` di bagian atas.
3. Masukkan daftar repositori Anda (pribadi maupun organisasi).
   ```python
   REPOSITORIES = [
       "username-anda/repo-pribadi",
       "organisasi-anda/repo-kerja"
   ]
   ```
4. Simpan file tersebut.

---

## 📤 Langkah 2: Unggah ke GitHub
Jika Anda belum membuat repositori di GitHub, buatlah satu (bisa Private atau Public). Kemudian jalankan perintah berikut di terminal Anda:

```bash
# Inisialisasi git (jika belum)
git init

# Tambahkan semua file
git add .

# Buat commit pertama
git commit -m "Initial commit: Setup Bot Aktivitas IWK"

# Hubungkan ke repo GitHub Anda
git remote add origin https://github.com/username-anda/nama-repo-bot.git

# Unggah kode
git push -u origin main
```

---

## 🔐 Langkah 3: Konfigurasi GitHub Secrets
GitHub Actions membutuhkan kunci akses Anda, tetapi kita tidak boleh menaruhnya di dalam kode. Kita akan menggunakan **Secrets**.

1. Buka repositori Anda di situs GitHub.
2. Klik tab **Settings** di bagian atas.
3. Di menu samping kiri, klik **Secrets and variables** > **Actions**.
4. Klik tombol **New repository secret**.
5. Masukkan kunci-kunci berikut satu per satu:

| Nama Secret | Nilai (Value) | Keterangan |
| :--- | :--- | :--- |
| `GITHUB_PAT` | `ghp_xxxx...` | Token akses GitHub Anda |
| `GEMINI_API_KEY` | `AIzaSy...` | API Key dari Google AI Studio |
| `TELEGRAM_BOT_TOKEN` | `123456:ABC...` | Token dari BotFather |
| `TELEGRAM_CHAT_ID` | `987654321` | ID chat Anda dari userinfobot |
| `GITHUB_USERNAME` | `username_anda` | **(Opsional)** Username GitHub Anda |

---

## 🕒 Langkah 4: Jadwal Otomatis
Bot ini sudah dikonfigurasi di `.github/workflows/daily-summary.yml` untuk berjalan:
- **Setiap Hari**: Pukul 11:00 UTC (Sama dengan **18:00 WIB**).
- **Manual**: Kapan pun Anda inginkan melalui tombol "Run Workflow".

---

## 🧪 Langkah 5: Uji Coba Deployment (Manual Run)
Jangan menunggu sampai jam 6 sore untuk tahu apakah bot bekerja. Anda bisa mencobanya sekarang:

1. Di repositori GitHub Anda, klik tab **Actions**.
2. Di sebelah kiri, klik nama workflow: **Daily Commit Summary**.
3. Klik tombol abu-abu **Run workflow** di sebelah kanan.
4. Klik tombol hijau **Run workflow** yang muncul di menu dropdown.
5. Tunggu sekitar 1 menit. Jika ikon centang hijau muncul, periksa Telegram Anda!

---

## 🛠 Troubleshooting (Jika Gagal)
Jika muncul tanda silang merah di tab Actions:
1. Klik pada nama run yang gagal tersebut.
2. Klik bagian **Run Summary Script** untuk melihat pesan error.
3. **Common Errors:**
   - `401 Unauthorized`: Periksa apakah `GITHUB_PAT` atau `GEMINI_API_KEY` sudah benar.
   - `404 Not Found`: Pastikan format repositori di `main.py` benar (`owner/repo`).
   - `SAML SSO`: Jika menggunakan repo organisasi, pastikan Token GitHub Anda sudah di-authorize untuk SSO.

---
**Kembali ke [README.md](README.md)**
