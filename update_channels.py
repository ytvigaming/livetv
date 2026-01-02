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
    "star plus", "star gold", "star bharat", "star उत्सव", "star utsav",
    "zee tv", "zee cinema", "zee bollywood", "zee action", "zee anmol", "zee classic", "&tv", "and tv",
    "sony", "set india", "sony max", "sony sab", "sony pal", "sony wah",
    "colors", "colors cineplex", "colors rishtey",
    "dangal", "shemaroo", "big magic", "manoranjan", "b4u", "filmy", "goldmines",
    
    # --- News ---
    "aaj tak", "abp", "india tv", "ndtv", "news18", "news 18", "news nation", 
    "republic", "tv9", "zee news", "times now", "cnbc", "good news", "sudarshan",
    "bharat24", "dd news", "sansad",
    
    # --- Sports ---
    "star sports", "sony ten", "sony six", "sports18", "sports 18", "dd sports", "eurosport",
    
    # --- South India ---
    "sun tv", "ktv", "sun news", "sun music", "adithya", "chutti",
    "gemini", "etv", "maa tv", "star maa", "zee telugu",
    "asianet", "surya", "mazhavil", "manorama", "mathrubhumi",
    "udaya", "zee kannada", "colors kannada", "public tv",
    "polimer", "thanthi", "puthiya thalaimurai", "kalaignar",
    
    # --- Regional ---
    "zee bangla", "star jalsha", "colors bangla", "abp ananda",
    "zee marathi", "colors marathi", "star pravah", "abp majha",
    "zee punjabi", "ptc", "mh1",
    "zee 24 kalak", "tv9 gujarati", "colors gujarati",
    "tarang", "sarthak", "zee sarthak",
    
    # --- Music & Lifestyle ---
    "mtv", "vh1", "zoom", "9xm", "masti", "zing", "music india", "e24",
    "tlc", "discovery", "history", "animal planet", "nat geo",
    
    # --- Devotional ---
    "aasta", "aastha", "sanskar", "sadhna", "paras", "arihant", "mh1 shraddha", "vedic",
    
    # --- Doordarshan (DD) ---
    "dd national", "dd bharati", "dd retro", "dd kisan", "dd urdu", "dd india",
    "dd bangla", "dd chandana", "dd girnar", "dd mp", "dd odia", "dd podhigai", 
    "dd punjabi", "dd rajasthan", "dd sahyadri", "dd saptagiri", "dd yadagiri"
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
