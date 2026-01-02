import requests
import re

# Sources: Jaha se channels dhundne hain
SOURCE_URLS = [
    "https://raw.githubusercontent.com/bugsfreeweb/LiveTVCollector/refs/heads/main/LiveTV/India/LiveTV.m3u"
]

# --- MANUAL LIST (WHITELIST) ---
# Script sirf inhi naamo wale channels ko add karega.
# Aap isme aur naam add kar sakte hain comma laga kar.
WANTED_CHANNELS = [
    # --- Hindi GEC & Movies ---
    "sony sab", "sony pal", "sony wah",
]

# --- BLOCK LIST (SAFETY FILTER) ---
# Ye words mile toh channel reject ho jayega
BLOCKED_KEYWORDS = [
    "adult", "xxx", "porn", "18+", "sex", "erotic", "uncensored", 
    "babes", "strip", "brazzers", "playboy", "hustler", "desimms"
]

# Output file ka naam
OUTPUT_FILE = "list"

def is_wanted_channel(channel_name):
    name_lower = channel_name.lower()
    
    # 1. Safety Check
    for bad in BLOCKED_KEYWORDS:
        if bad in name_lower:
            return False

    # 2. Whitelist Check
    for wanted in WANTED_CHANNELS:
        if wanted in name_lower:
            return True
            
    return False

def update_list():
    unique_channels = {}
    print("Fetching channels from sources...")
    
    for url in SOURCE_URLS:
        try:
            print(f"Downloading: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                content = response.text
                lines = content.split('\n')
                current_info = ""
                
                for line in lines:
                    line = line.strip()
                    if not line: continue
                        
                    if line.startswith("#EXTINF"):
                        current_info = line
                    elif not line.startswith("#") and current_info != "":
                        try:
                            channel_name = current_info.split(',')[-1].strip()
                        except:
                            channel_name = "Unknown"
                        
                        if is_wanted_channel(channel_name):
                            if channel_name not in unique_channels:
                                unique_channels[channel_name] = {
                                    'info': current_info,
                                    'url': line
                                }
                        current_info = "" 
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        count = 0
        for name in sorted(unique_channels.keys()):
            entry = unique_channels[name]
            f.write(f"{entry['info']}\n")
            f.write(f"{entry['url']}\n")
            count += 1
            
    print(f"Success! Total matched Indian channels found: {count}")

if __name__ == "__main__":
    update_list()
