import os
import requests
from datetime import datetime, timedelta, timezone

# --- KONFIGURASI ---
# Tambahkan daftar repositori yang ingin Anda pantau (format: "owner/repo")
REPOSITORIES = [
    "iweka-dev/nursery-oil-palm-be", 
    "iweka-dev/admin-be"
]

# Variabel Lingkungan (Akan diisi oleh GitHub Secrets)
GH_PAT = os.getenv("GH_PAT")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

# Username GitHub Anda (Gunakan secret GH_USERNAME jika berbeda dengan akun tempat bot berada)
GITHUB_USERNAME = os.getenv("GH_USERNAME") or os.getenv("GH_REPOSITORY_OWNER")

def get_time_range():
    """Mendapatkan waktu sekarang dan 12 jam yang lalu dalam format ISO 8601."""
    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=12)
    return since.strftime("%Y-%m-%dT%H:%M:%SZ")

def fetch_commits(repo, since):
    """Mengambil pesan komit dari GitHub API."""
    url = f"https://api.github.com/repos/{repo}/commits"
    headers = {
        "Authorization": f"Bearer {GH_PAT}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {
        "author": GITHUB_USERNAME,
        "since": since
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        commits = response.json()
        return [c["commit"]["message"] for c in commits]
    except Exception as e:
        print(f"Error saat mengambil komit dari {repo}: {e}")
        return []

def summarize_with_openrouter(commits_text):
    """Merangkum pesan komit menggunakan OpenRouter Chat Completions API."""
    if not commits_text.strip():
        return "Tidak ada aktivitas komit yang ditemukan dalam 12 jam terakhir."
    
    # Mendapatkan hari dan tanggal hari ini dalam Bahasa Indonesia
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    now = datetime.now()
    hari_ini = days[now.weekday()]
    tanggal_ini = f"{now.day} {months[now.month - 1]} {now.year}"
    
    system_prompt = (
        f"Anda adalah asisten pengembang perangkat lunak senior yang profesional. "
        f"Tugas Anda adalah merangkum daftar pesan komit mentah menjadi laporan harian untuk Project Manager dalam Bahasa Indonesia yang formal.\n\n"
        f"Aturan Penulisan:\n"
        f"1. Baris pertama WAJIB berisi: 'Laporan Aktivitas Harian - {hari_ini}, {tanggal_ini}'.\n"
        f"2. Kelompokkan rangkuman berdasarkan repositori sesuai input (gunakan format: ### [Nama Repo]).\n"
        f"3. Fokus pada perubahan fungsionalitas, perbaikan bug, atau optimasi. Abaikan komit minor (typo, readme, dll).\n"
        f"4. Setiap poin pekerjaan menggunakan bullet point '*' dan WAJIB diakhiri dengan frase ' - done'.\n"
        f"5. Gunakan bahasa yang profesional dan mudah dipahami oleh Project Manager (hindari jargon teknis yang terlalu mentah)."
    )
    
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Berikut adalah daftar pesan komit saya yang dikelompokkan per repo:\n\n{commits_text}"
                }
            ],
            "temperature": 0.3
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Gagal merangkum dengan OpenRouter: {e}"

def send_to_telegram(message):
    """Mengirim pesan ke Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🚀 *Daily Commit Summary*\n\n{message}",
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Pesan berhasil dikirim ke Telegram!")
    except Exception as e:
        print(f"Gagal mengirim pesan ke Telegram: {e}")

def main():
    since = get_time_range()
    formatted_input = []
    
    print(f"Memulai ekstraksi komit sejak {since}...")
    
    for repo in REPOSITORIES:
        repo_name_only = repo.split("/")[-1]
        print(f"Memeriksa repositori: {repo}")
        messages = fetch_commits(repo, since)
        
        if messages:
            repo_block = f"### REPOSITORY: {repo_name_only}\n"
            repo_block += "\n".join([f"- {m}" for m in messages])
            formatted_input.append(repo_block)
    
    if not formatted_input:
        print("Tidak ada komit baru di semua repositori.")
        summary = "Tidak ada aktivitas komit yang ditemukan dalam 12 jam terakhir."
    else:
        # Gabungkan semua blok repo dengan pemisah baris baru
        combined_input = "\n\n".join(formatted_input)
        print("Merangkum dengan AI...")
        summary = summarize_with_openrouter(combined_input)
    
    print("Mengirim ke Telegram...")
    send_to_telegram(summary)

if __name__ == "__main__":
    main()
