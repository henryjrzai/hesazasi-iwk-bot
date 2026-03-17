# 🔑 Panduan Mendapatkan API Key & Token

Dokumen ini akan membimbing Anda langkah-demi-langkah untuk mendapatkan 4 kredensial yang dibutuhkan agar bot ini dapat berjalan.

---

## 1. GitHub Personal Access Token (PAT)
Token ini digunakan agar bot dapat membaca daftar komit dari repositori Anda.

1.  Buka **[GitHub Settings > Developer Settings](https://github.com/settings/apps)**.
2.  Pilih **Personal access tokens** > **Fine-grained tokens**.
3.  Klik **Generate new token**.
4.  Isi nama token (contoh: `Bot-Aktivitas-Token`).
5.  Pada bagian **Repository access**, pilih:
    - **All repositories** (jika ingin memantau semua repo).
    - **Only select repositories** (pilih repo tertentu saja).
6.  Pada bagian **Permissions**, cari **Contents** dan ubah menjadi **Read-only**.
7. Klik **Generate token** dan **SIMPAN** kodenya segera (karena hanya muncul sekali).

---

## 🏢 Akses Repositori Organisasi (Sangat Penting)
Jika repositori yang ingin Anda pantau milik organisasi:

1.  **SAML SSO:** Jika organisasi menggunakan SSO, cari tombol **Configure SSO** di sebelah token yang baru Anda buat (di daftar token), lalu klik **Authorize** untuk setiap organisasi yang dibutuhkan.
2.  **Fine-grained Token:** Pastikan **Resource owner** diatur ke organisasi tersebut jika organisasi membatasi akses token.
3.  **GITHUB_USERNAME:** Pastikan Anda mengisi rahasia `GITHUB_USERNAME` dengan username pribadi Anda (bukan nama organisasi) agar filter komit bekerja dengan benar.

---

## 2. Google Gemini API Key
Token ini digunakan untuk mengakses kecerdasan buatan Gemini guna merangkum pesan komit.

1.  Buka **[Google AI Studio](https://aistudio.google.com/)**.
2.  Login menggunakan akun Google Anda.
3.  Di bilah sisi kiri, klik tombol **Get API key**.
4.  Klik **Create API key in new project**.
5.  Salin kode API Key yang muncul (berawalan `AIzaSy...`).

---

## 3. Telegram Bot Token
Token ini digunakan untuk mengontrol bot Telegram yang akan mengirim pesan ke Anda.

1.  Buka aplikasi Telegram dan cari bot bernama **[@BotFather](https://t.me/botfather)**.
2.  Ketik perintah `/newbot`.
3.  Ikuti instruksi:
    - Masukkan **Display Name** bot Anda (contoh: `My Activity Bot`).
    - Masukkan **Username** bot (harus diakhiri dengan kata `_bot`, contoh: `iwk_summary_bot`).
4.  Setelah selesai, Anda akan menerima pesan berisi **HTTP API Token** (contoh: `123456789:ABCDefgh...`). Simpan token ini.

---

## 4. Telegram Chat ID
ID ini unik untuk setiap akun Telegram, sehingga bot tahu ke mana harus mengirim laporan (ke Anda, bukan orang lain).

1.  Cari bot bernama **[@userinfobot](https://t.me/userinfobot)** di Telegram.
2.  Klik **Start**.
3.  Bot tersebut akan membalas dengan informasi profil Anda.
4.  Salin angka yang ada di baris **Id** (contoh: `987654321`).

---

## 🛠 Cara Memasukkan ke GitHub Secrets

Setelah mendapatkan semua kunci di atas, masukkan ke repositori GitHub Anda:

1.  Buka Repositori Anda di GitHub.
2.  Klik **Settings** (tab atas).
3.  Di menu kiri, klik **Secrets and variables** > **Actions**.
4.  Klik tombol hijau **New repository secret**.
5.  Masukkan nama rahasia (contoh: `GITHUB_PAT`) dan tempel kodenya.
6.  Ulangi untuk keempat kunci tersebut sesuai tabel di `README.md`.

---
**💡 Tips Keamanan:** Jangan pernah membagikan kunci-kunci ini kepada siapa pun atau menaruhnya langsung di dalam kode program (`main.py`). Gunakan selalu file `.env` untuk lokal atau GitHub Secrets untuk online.
