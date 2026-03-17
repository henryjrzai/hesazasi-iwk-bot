import os
import requests
from datetime import datetime, timedelta, timezone
from google import genai

# --- KONFIGURASI ---
# Tambahkan daftar repositori yang ingin Anda pantau (format: "owner/repo")
REPOSITORIES = ["username/repo1", "username/repo2"]

# Variabel Lingkungan (Akan diisi oleh GitHub Secrets)
GITHUB_PAT = os.getenv("GITHUB_PAT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Username GitHub Anda (Gunakan secret GITHUB_USERNAME jika berbeda dengan akun tempat bot berada)
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME") or os.getenv("GITHUB_REPOSITORY_OWNER")

def get_time_range():
    """Mendapatkan waktu sekarang dan 12 jam yang lalu dalam format ISO 8601."""
    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=12)
    return since.strftime("%Y-%m-%dT%H:%M:%SZ")

def fetch_commits(repo, since):
    """Mengambil pesan komit dari GitHub API."""
    url = f"https://api.github.com/repos/{repo}/commits"
    headers = {
        "Authorization": f"Bearer {GITHUB_PAT}",
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

def summarize_with_gemini(commits_text):
    """Merangkum pesan komit menggunakan SDK google-genai."""
    if not commits_text.strip():
        return "Tidak ada aktivitas komit yang ditemukan dalam 12 jam terakhir."

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    system_prompt = (
        "Anda adalah asisten pengembang perangkat lunak senior yang profesional. "
        "Tugas Anda adalah merangkum daftar pesan komit mentah menjadi laporan harian yang ringkas dalam Bahasa Indonesia. "
        "Abaikan komit yang terlalu minor seperti 'update readme', 'typo', atau 'bump version'. "
        "Kelompokkan rangkuman ke dalam kategori seperti: Perbaikan Bug, Penambahan Fitur, Refaktor, dll. "
        "Gunakan poin-poin (bullet points) dan pastikan nada bicara profesional namun mudah dibaca."
    )
    
    try:
        # Menggunakan model gemini-2.0-flash (silakan ganti ke 2.5 jika tersedia)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Berikut adalah daftar pesan komit saya:\n\n{commits_text}",
            config={
                "system_instruction": system_prompt,
                "temperature": 0.2
            }
        )
        return response.text
    except Exception as e:
        return f"Gagal merangkum dengan Gemini: {e}"

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
    all_commit_messages = []
    
    print(f"Memulai ekstraksi komit sejak {since}...")
    
    for repo in REPOSITORIES:
        print(f"Memeriksa repositori: {repo}")
        messages = fetch_commits(repo, since)
        all_commit_messages.extend(messages)
    
    # Gabungkan semua pesan menjadi satu teks besar
    combined_text = "\n".join([f"- {m}" for m in all_commit_messages])
    
    print("Merangkum dengan AI...")
    summary = summarize_with_gemini(combined_text)
    
    print("Mengirim ke Telegram...")
    send_to_telegram(summary)

if __name__ == "__main__":
    main()
