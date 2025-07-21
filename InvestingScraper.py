import requests
from bs4 import BeautifulSoup

def scrape_investing():
    url = "https://br.investing.com/technical/personalized-quotes-technical-summary"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find("table")
    rows = table.find_all("tr")[1:]

    signals = {}
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 7:
            continue
        pair = cols[0].text.strip()
        signals[pair] = {
            "5M": cols[3].text.strip(),
            "15M": cols[4].text.strip(),
            "1H": cols[5].text.strip(),
            "Diário": cols[6].text.strip()
        }
    return signals
