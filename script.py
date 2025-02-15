import requests
import re
import json

def fetch_page_source(url):
    headers = {
        'Connection': 'keep-alive',
        'Origin': 'https://stylisheleg4nt.com',
        'Referer': 'https://stream.crichd.vip/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def decode_url(url):
    url = url.replace('\\', '').strip()
    if not url.startswith(('https://', 'http://')):
        url = 'https://' + url
    return re.sub(r'https:/+', 'https://', url)

channels = [
    {"name": "SSC | Extra 02", "id": "ptvpk", "logo": "https://cdn.jsdelivr.net/gh/HelloPeopleTv4you/IPTV-Playlist@406da1fce47b6a0b713d4893c7c633b4bee2b645/img/SSC-Extra-2-300x188.png"},
    {"name": "SSC | Extra 01", "id": "Extra01", "logo": "https://cdn.jsdelivr.net/gh/HelloPeopleTv4you/IPTV-Playlist@406da1fce47b6a0b713d4893c7c633b4bee2b645/img/SSC-Extra-1-300x188.png"}
]

result = []
m3u_content = "#EXTM3U\n"

for channel in channels:
    url = f"https://stylisheleg4nt.com/premium.php?player=mobile&live={channel['id']}"
    response = fetch_page_source(url)
    
    if response and (match := re.search(r'return\(\[(.*?)\]\.join', response)):
        url_parts = match.group(1).replace('"', '').split(',')
        final_content = ''.join(url_parts)
        link = decode_url(final_content)
        
        result.append({
            "name": channel["name"],
            "logo": channel["logo"],
            "url": link,
            "referer": "https://stylisheleg4nt.com",
            "origin": "https://stylisheleg4nt.com"
        })
        
        # Add custom HTTP headers and channel to M3U playlist
        m3u_content += (
            f'#EXTHTTP:{{"Origin":"https://stylisheleg4nt.com","Referer":"https://stylisheleg4nt.com/"}}\n'
            f'#EXTINF:-1 tvg-logo="{channel["logo"]}", {channel["name"]}\n{link}\n'
        )
    else:
        result.append({
            "name": channel["name"],
            "logo": channel["logo"],
            "error": "Token not found or failed to fetch."
        })

# Save the result as result.json
with open("NS_player.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

# Save the M3U playlist as NS_player.m3u
with open("ALL.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)
