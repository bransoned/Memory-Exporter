#from bs4 import BeautifulSoup
import re

def parse_snapchat_memories(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    rows = soup.find_all("tr")[1:]  # skip header row

    memories = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        # Extract basic text fields
        date_str = cells[0].get_text(strip=True)
        media_type = cells[1].get_text(strip=True)

        # Extract location
        loc_text = cells[2].get_text(strip=True)
        lat, lon = None, None
        if "Latitude" in loc_text:
            match = re.search(r"([-0-9.]+),\s*([-0-9.]+)", loc_text)
            if match:
                lat, lon = match.groups()

        # Extract URL from onclick attribute
        link_tag = cells[3].find("a")
        link = None

        if link_tag and "onclick" in link_tag.attrs:
            onclick = link_tag["onclick"]
            # Extract the URL inside downloadMemories('URL', ...)
            match = re.search(r"downloadMemories\('([^']+)'", onclick)
            if match:
                link = match.group(1)

        memories.append({
            "date": date_str,
            "type": media_type,
            "lat": lat,
            "lon": lon,
            "url": link
        })

    return memories

if __name__ == "__main__":


    target_string = "<div id='mem-info-bar'"

    with open("memories_history.html", "r") as file:
        for line in file:
            if target_string in line:
                html_text = line


    print(html_text)
#    print(parse_snapchat_memories(html_text))
