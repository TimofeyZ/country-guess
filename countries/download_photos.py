#!/usr/bin/env python3
"""Download up to four representative photos per new country from Wikimedia Commons.
Run this file from the main extracted folder; Python 3 is enough, no pip packages required.
"""
from __future__ import annotations
import csv, json, mimetypes, re, sys, time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "CountryPhotoDatasetBuilder/1.0 (educational photo dataset)"
PHOTOS_PER_COUNTRY = 4
IMAGE_EXTENSIONS = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
SKIP_WORDS = ("flag", "map of", "coat of arms", "logo", "icon", "emblem", "locator map", "blank map")
COUNTRIES = [
  {
    "name": "Argentina",
    "folder": "iguazu_falls",
    "queries": [
      "Iguazu Falls",
      "La Boca Buenos Aires"
    ]
  },
  {
    "name": "Australia",
    "folder": "australia",
    "queries": [
      "Sydney Opera House",
      "Uluru Australia"
    ]
  },
  {
    "name": "Austria",
    "folder": "austria",
    "queries": [
      "Schönbrunn Palace Vienna",
      "Hallstatt Austria"
    ]
  },
  {
    "name": "Azerbaijan",
    "folder": "azerbaijan",
    "queries": [
      "Flame Towers Baku",
      "Gobustan Azerbaijan"
    ]
  },
  {
    "name": "Bangladesh",
    "folder": "bangladesh",
    "queries": [
      "Sundarbans Bangladesh",
      "Lalbagh Fort Dhaka"
    ]
  },
  {
    "name": "Belarus",
    "folder": "belarus",
    "queries": [
      "Mir Castle Belarus",
      "Minsk Belarus city"
    ]
  },
  {
    "name": "Belgium",
    "folder": "belgium",
    "queries": [
      "Grand Place Brussels",
      "Bruges canals Belgium"
    ]
  },
  {
    "name": "Bolivia",
    "folder": "bolivia",
    "queries": [
      "Salar de Uyuni",
      "Tiwanaku Bolivia"
    ]
  },
  {
    "name": "Bosnia and Herzegovina",
    "folder": "bosnia_and_herzegovina",
    "queries": [
      "Stari Most Mostar",
      "Sarajevo old town"
    ]
  },
  {
    "name": "Botswana",
    "folder": "botswana",
    "queries": [
      "Okavango Delta",
      "Chobe National Park Botswana"
    ]
  },
  {
    "name": "Brazil",
    "folder": "brazil",
    "queries": [
      "Christ the Redeemer Rio de Janeiro",
      "Iguazu Falls Brazil"
    ]
  },
  {
    "name": "Bulgaria",
    "folder": "bulgaria",
    "queries": [
      "Rila Monastery",
      "Plovdiv old town Bulgaria"
    ]
  },
  {
    "name": "Cambodia",
    "folder": "cambodia",
    "queries": [
      "Angkor Wat Cambodia",
      "Tonle Sap Cambodia"
    ]
  },
  {
    "name": "Chile",
    "folder": "chile",
    "queries": [
      "Torres del Paine",
      "Atacama Desert Chile"
    ]
  },
  {
    "name": "China",
    "folder": "china",
    "queries": [
      "Great Wall of China",
      "Forbidden City Beijing"
    ]
  },
  {
    "name": "Colombia",
    "folder": "colombia",
    "queries": [
      "Cartagena Colombia old town",
      "Cocora Valley Colombia"
    ]
  },
  {
    "name": "Costa Rica",
    "folder": "costa_rica",
    "queries": [
      "Arenal Volcano Costa Rica",
      "Monteverde cloud forest"
    ]
  },
  {
    "name": "Croatia",
    "folder": "croatia",
    "queries": [
      "Dubrovnik old town",
      "Plitvice Lakes Croatia"
    ]
  },
  {
    "name": "Cuba",
    "folder": "cuba",
    "queries": [
      "Old Havana Cuba",
      "Vinales Valley Cuba"
    ]
  },
  {
    "name": "Cyprus",
    "folder": "cyprus",
    "queries": [
      "Paphos archaeological park Cyprus",
      "Nicosia old town Cyprus"
    ]
  },
  {
    "name": "Czech Republic",
    "folder": "czech_republic",
    "queries": [
      "Prague Castle Czech Republic",
      "Charles Bridge Prague"
    ]
  },
  {
    "name": "Denmark",
    "folder": "denmark",
    "queries": [
      "Nyhavn Copenhagen",
      "Kronborg Castle Denmark"
    ]
  },
  {
    "name": "Dominican Republic",
    "folder": "dominican_republic",
    "queries": [
      "Santo Domingo Colonial Zone",
      "Punta Cana Dominican Republic"
    ]
  },
  {
    "name": "Ecuador",
    "folder": "ecuador",
    "queries": [
      "Galapagos Islands Ecuador",
      "Quito historic center"
    ]
  },
  {
    "name": "Estonia",
    "folder": "estonia",
    "queries": [
      "Tallinn old town Estonia",
      "Lahemaa National Park Estonia"
    ]
  },
  {
    "name": "Ethiopia",
    "folder": "ethiopia",
    "queries": [
      "Lalibela rock-hewn churches",
      "Simien Mountains Ethiopia"
    ]
  },
  {
    "name": "Finland",
    "folder": "finland",
    "queries": [
      "Suomenlinna Helsinki",
      "Lapland Finland landscape"
    ]
  },
  {
    "name": "France",
    "folder": "france",
    "queries": [
      "Eiffel Tower Paris",
      "Mont Saint-Michel France"
    ]
  },
  {
    "name": "Georgia",
    "folder": "georgia",
    "queries": [
      "Gergeti Trinity Church Georgia",
      "Tbilisi old town Georgia"
    ]
  },
  {
    "name": "Ghana",
    "folder": "ghana",
    "queries": [
      "Cape Coast Castle Ghana",
      "Kakum National Park Ghana"
    ]
  },
  {
    "name": "Greece",
    "folder": "greece",
    "queries": [
      "Acropolis Athens Greece",
      "Santorini Oia Greece"
    ]
  },
  {
    "name": "Guatemala",
    "folder": "guatemala",
    "queries": [
      "Tikal Guatemala",
      "Antigua Guatemala historic center"
    ]
  },
  {
    "name": "Hungary",
    "folder": "hungary",
    "queries": [
      "Hungarian Parliament Budapest",
      "Fishermans Bastion Budapest"
    ]
  },
  {
    "name": "Iceland",
    "folder": "iceland",
    "queries": [
      "Kirkjufell Iceland",
      "Skogafoss Iceland"
    ]
  },
  {
    "name": "Indonesia",
    "folder": "indonesia",
    "queries": [
      "Borobudur Indonesia",
      "Bali rice terraces Indonesia"
    ]
  },
  {
    "name": "Iran",
    "folder": "iran",
    "queries": [
      "Persepolis Iran",
      "Nasir al-Mulk Mosque Shiraz"
    ]
  },
  {
    "name": "Iraq",
    "folder": "iraq",
    "queries": [
      "Erbil Citadel Iraq",
      "Ziggurat of Ur Iraq"
    ]
  },
  {
    "name": "Ireland",
    "folder": "ireland",
    "queries": [
      "Cliffs of Moher Ireland",
      "Trinity College Dublin Ireland"
    ]
  },
  {
    "name": "Japan",
    "folder": "japan",
    "queries": [
      "Mount Fuji Japan",
      "Fushimi Inari Shrine Kyoto"
    ]
  },
  {
    "name": "Jordan",
    "folder": "jordan",
    "queries": [
      "Petra Jordan",
      "Wadi Rum Jordan"
    ]
  },
  {
    "name": "Kazakhstan",
    "folder": "kazakhstan",
    "queries": [
      "Charyn Canyon Kazakhstan",
      "Bayterek Tower Astana"
    ]
  },
  {
    "name": "Kenya",
    "folder": "kenya",
    "queries": [
      "Maasai Mara Kenya",
      "Mount Kenya landscape"
    ]
  },
  {
    "name": "Laos",
    "folder": "laos",
    "queries": [
      "Luang Prabang Laos",
      "Kuang Si Falls Laos"
    ]
  },
  {
    "name": "Latvia",
    "folder": "latvia",
    "queries": [
      "Riga old town Latvia",
      "Rundale Palace Latvia"
    ]
  },
  {
    "name": "Lebanon",
    "folder": "lebanon",
    "queries": [
      "Baalbek Roman ruins Lebanon",
      "Jeita Grotto Lebanon"
    ]
  },
  {
    "name": "Lithuania",
    "folder": "lithuania",
    "queries": [
      "Vilnius old town Lithuania",
      "Trakai Island Castle Lithuania"
    ]
  },
  {
    "name": "Madagascar",
    "folder": "madagascar",
    "queries": [
      "Avenue of the Baobabs Madagascar",
      "Tsingy de Bemaraha Madagascar"
    ]
  },
  {
    "name": "Malaysia",
    "folder": "malaysia",
    "queries": [
      "Petronas Twin Towers Kuala Lumpur",
      "Langkawi Malaysia landscape"
    ]
  },
  {
    "name": "Maldives",
    "folder": "maldives",
    "queries": [
      "Maldives atolls aerial",
      "Male Grand Friday Mosque Maldives"
    ]
  },
  {
    "name": "Malta",
    "folder": "malta",
    "queries": [
      "Valletta Malta old town",
      "Mdina Malta"
    ]
  },
  {
    "name": "Mongolia",
    "folder": "mongolia",
    "queries": [
      "Gobi Desert Mongolia",
      "Erdene Zuu Monastery Mongolia"
    ]
  },
  {
    "name": "Morocco",
    "folder": "morocco",
    "queries": [
      "Chefchaouen Morocco",
      "Ait Benhaddou Morocco"
    ]
  },
  {
    "name": "Myanmar",
    "folder": "myanmar",
    "queries": [
      "Bagan temples Myanmar",
      "Shwedagon Pagoda Yangon"
    ]
  },
  {
    "name": "Namibia",
    "folder": "namibia",
    "queries": [
      "Sossusvlei dunes Namibia",
      "Etosha National Park Namibia"
    ]
  },
  {
    "name": "Nepal",
    "folder": "nepal",
    "queries": [
      "Mount Everest Nepal",
      "Boudhanath Stupa Kathmandu"
    ]
  },
  {
    "name": "Netherlands",
    "folder": "netherlands",
    "queries": [
      "Amsterdam canals Netherlands",
      "Kinderdijk windmills Netherlands"
    ]
  },
  {
    "name": "New Zealand",
    "folder": "new_zealand",
    "queries": [
      "Milford Sound New Zealand",
      "Aoraki Mount Cook New Zealand"
    ]
  },
  {
    "name": "Nigeria",
    "folder": "nigeria",
    "queries": [
      "Zuma Rock Nigeria",
      "Olumo Rock Nigeria"
    ]
  },
  {
    "name": "Norway",
    "folder": "norway",
    "queries": [
      "Geirangerfjord Norway",
      "Lofoten Islands Norway"
    ]
  },
  {
    "name": "Oman",
    "folder": "oman",
    "queries": [
      "Sultan Qaboos Grand Mosque Oman",
      "Wahiba Sands Oman"
    ]
  },
  {
    "name": "Pakistan",
    "folder": "pakistan",
    "queries": [
      "Badshahi Mosque Lahore Pakistan",
      "Hunza Valley Pakistan"
    ]
  },
  {
    "name": "Panama",
    "folder": "panama",
    "queries": [
      "Panama Canal Panama",
      "Casco Viejo Panama City"
    ]
  },
  {
    "name": "Paraguay",
    "folder": "paraguay",
    "queries": [
      "La Santisima Trinidad Jesuit Missions Paraguay",
      "Itaipu Dam Paraguay"
    ]
  },
  {
    "name": "Peru",
    "folder": "peru",
    "queries": [
      "Machu Picchu Peru",
      "Vinicunca Rainbow Mountain Peru"
    ]
  },
  {
    "name": "Philippines",
    "folder": "philippines",
    "queries": [
      "Chocolate Hills Philippines",
      "Banaue Rice Terraces Philippines"
    ]
  },
  {
    "name": "Poland",
    "folder": "poland",
    "queries": [
      "Wawel Castle Krakow Poland",
      "Warsaw old town Poland"
    ]
  },
  {
    "name": "Portugal",
    "folder": "portugal",
    "queries": [
      "Belem Tower Lisbon Portugal",
      "Porto Ribeira Portugal"
    ]
  },
  {
    "name": "Romania",
    "folder": "romania",
    "queries": [
      "Bran Castle Romania",
      "Peles Castle Romania"
    ]
  },
  {
    "name": "Saudi Arabia",
    "folder": "saudi_arabia",
    "queries": [
      "Hegra AlUla Saudi Arabia",
      "Kingdom Centre Riyadh Saudi Arabia"
    ]
  },
  {
    "name": "Senegal",
    "folder": "senegal",
    "queries": [
      "African Renaissance Monument Dakar",
      "Goree Island Senegal"
    ]
  },
  {
    "name": "Serbia",
    "folder": "serbia",
    "queries": [
      "Belgrade Fortress Serbia",
      "Petrovaradin Fortress Novi Sad"
    ]
  },
  {
    "name": "Singapore",
    "folder": "singapore",
    "queries": [
      "Marina Bay Sands Singapore",
      "Gardens by the Bay Singapore"
    ]
  },
  {
    "name": "Slovakia",
    "folder": "slovakia",
    "queries": [
      "High Tatras Slovakia",
      "Bratislava Castle Slovakia"
    ]
  },
  {
    "name": "Slovenia",
    "folder": "slovenia",
    "queries": [
      "Lake Bled Slovenia",
      "Postojna Cave Slovenia"
    ]
  },
  {
    "name": "South Africa",
    "folder": "south_africa",
    "queries": [
      "Table Mountain Cape Town",
      "Kruger National Park South Africa"
    ]
  },
  {
    "name": "South Korea",
    "folder": "south_korea",
    "queries": [
      "Gyeongbokgung Palace Seoul",
      "Jeju Island South Korea"
    ]
  },
  {
    "name": "Spain",
    "folder": "spain",
    "queries": [
      "Sagrada Familia Barcelona",
      "Alhambra Granada Spain"
    ]
  },
  {
    "name": "Sri Lanka",
    "folder": "sri_lanka",
    "queries": [
      "Sigiriya Sri Lanka",
      "Temple of the Tooth Kandy Sri Lanka"
    ]
  },
  {
    "name": "Sweden",
    "folder": "sweden",
    "queries": [
      "Gamla Stan Stockholm Sweden",
      "Icehotel Jukkasjarvi Sweden"
    ]
  },
  {
    "name": "Switzerland",
    "folder": "switzerland",
    "queries": [
      "Matterhorn Switzerland",
      "Chapel Bridge Lucerne Switzerland"
    ]
  },
  {
    "name": "Thailand",
    "folder": "thailand",
    "queries": [
      "Grand Palace Bangkok Thailand",
      "Phi Phi Islands Thailand"
    ]
  },
  {
    "name": "Tunisia",
    "folder": "tunisia",
    "queries": [
      "Amphitheatre of El Jem Tunisia",
      "Sidi Bou Said Tunisia"
    ]
  },
  {
    "name": "Turkey",
    "folder": "turkey",
    "queries": [
      "Hagia Sophia Istanbul Turkey",
      "Cappadocia Turkey landscape"
    ]
  },
  {
    "name": "Ukraine",
    "folder": "ukraine",
    "queries": [
      "Saint Sophia Cathedral Kyiv Ukraine",
      "Lviv old town Ukraine"
    ]
  },
  {
    "name": "United Arab Emirates",
    "folder": "united_arab_emirates",
    "queries": [
      "Burj Khalifa Dubai UAE",
      "Sheikh Zayed Grand Mosque Abu Dhabi"
    ]
  },
  {
    "name": "United Kingdom",
    "folder": "united_kingdom",
    "queries": [
      "Tower Bridge London UK",
      "Giant Causeway Northern Ireland"
    ]
  },
  {
    "name": "Uruguay",
    "folder": "uruguay",
    "queries": [
      "Colonia del Sacramento Uruguay",
      "Punta del Este Uruguay"
    ]
  },
  {
    "name": "Vatican City",
    "folder": "vatican_city",
    "queries": [
      "Saint Peters Basilica Vatican City",
      "Vatican Museums Vatican City"
    ]
  },
  {
    "name": "Vietnam",
    "folder": "vietnam",
    "queries": [
      "Ha Long Bay Vietnam",
      "Hoi An ancient town Vietnam"
    ]
  },
  {
    "name": "Zambia",
    "folder": "zambia",
    "queries": [
      "Victoria Falls Zambia",
      "South Luangwa National Park Zambia"
    ]
  },
  {
    "name": "Zimbabwe",
    "folder": "zimbabwe",
    "queries": [
      "Great Zimbabwe ruins",
      "Victoria Falls Zimbabwe"
    ]
  },
  {
    "name": "Egypt",
    "folder": "egypt",
    "queries": [
      "Pyramids of Giza Egypt",
      "Abu Simbel Egypt"
    ]
  }
]
CREDITS_PATH = Path(__file__).resolve().parent / "photo_credits.csv"


def request_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=35) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_candidates(query: str) -> list[dict]:
    params = {
        "action": "query", "format": "json", "formatversion": "2",
        "generator": "search", "gsrsearch": query, "gsrnamespace": "6", "gsrlimit": "25",
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata", "iiurlwidth": "1000",
    }
    data = request_json(API + "?" + urlencode(params))
    return data.get("query", {}).get("pages", [])


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", value).strip()


def file_extension(info: dict) -> str:
    mime = info.get("thumbmime") or info.get("mime") or "image/jpeg"
    return IMAGE_EXTENSIONS.get(mime, ".jpg")


def read_credits() -> list[dict]:
    if not CREDITS_PATH.exists():
        return []
    try:
        with CREDITS_PATH.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    except OSError:
        return []


def append_credit(row: dict) -> None:
    fields = ["country", "file", "commons_page", "author", "license", "source_file_url"]
    exists = CREDITS_PATH.exists()
    with CREDITS_PATH.open("a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def download_one(page: dict, destination: Path, country_name: str) -> bool:
    title = page.get("title", "")
    if any(word in title.lower() for word in SKIP_WORDS):
        return False
    infos = page.get("imageinfo") or []
    if not infos:
        return False
    info = infos[0]
    mime = info.get("mime", "")
    if mime not in IMAGE_EXTENSIONS:
        return False
    image_url = info.get("thumburl") or info.get("url")
    if not image_url:
        return False
    ext = file_extension(info)
    # Keep the folder naming convention from the supplied sample: 0 (1).jpg, 0 (2).jpg, ...
    index = 1
    while True:
        target = destination / f"0 ({index}){ext}"
        if not target.exists():
            break
        index += 1
    req = Request(image_url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=45) as response:
            blob = response.read(18 * 1024 * 1024 + 1)
        if len(blob) < 5000 or len(blob) > 18 * 1024 * 1024:
            return False
        # Basic file signature validation so HTML error pages are not saved as photos.
        if not (blob.startswith(b"\xff\xd8\xff") or blob.startswith(b"\x89PNG\r\n\x1a\n") or blob[:4] == b"RIFF"):
            return False
        target.write_bytes(blob)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        print(f"    download skipped: {title} ({exc})")
        return False
    meta = info.get("extmetadata") or {}
    author = clean_text((meta.get("Artist") or {}).get("value", ""))
    license_name = clean_text((meta.get("LicenseShortName") or {}).get("value", ""))
    page_url = info.get("descriptionurl", "")
    append_credit({"country": country_name, "file": str(target.relative_to(Path(__file__).resolve().parent)),
                   "commons_page": page_url, "author": author, "license": license_name,
                   "source_file_url": info.get("url", "")})
    print(f"    saved {target.name}: {title}")
    return True


def main() -> int:
    base = Path(__file__).resolve().parent
    countries = COUNTRIES
    total = len(countries)
    failures = 0
    print(f"Photo download: up to {PHOTOS_PER_COUNTRY} images for {total} country folders.\n")
    for counter, country in enumerate(countries, 1):
        folder = base / country["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        existing_images = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
        if len(existing_images) >= PHOTOS_PER_COUNTRY:
            print(f"[{counter}/{total}] {country['name']}: already has {len(existing_images)} photos; leaving intact")
            continue
        print(f"[{counter}/{total}] {country['name']}")
        used_titles = set()
        # Query each of two landmarks; aim for two photos per landmark to get variety.
        goal = PHOTOS_PER_COUNTRY
        count = len(existing_images)
        for q_index, landmark in enumerate(country["queries"]):
            query = f"{landmark} {country['name']}"
            try:
                pages = fetch_candidates(query)
            except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
                print(f"    search temporarily failed for '{query}': {exc}")
                failures += 1
                continue
            added_this_query = 0
            for page in pages:
                title = page.get("title", "")
                if title in used_titles:
                    continue
                used_titles.add(title)
                if download_one(page, folder, country["name"]):
                    count += 1
                    added_this_query += 1
                    if count >= goal or added_this_query >= 2:
                        break
            time.sleep(0.35)
            if count >= goal:
                break
        # If fewer than four were available from landmark searches, try a broad country photo query.
        if count < goal:
            try:
                pages = fetch_candidates(f"{country['name']} landscape city landmark")
                for page in pages:
                    if page.get("title") in used_titles:
                        continue
                    used_titles.add(page.get("title"))
                    if download_one(page, folder, country["name"]):
                        count += 1
                        if count >= goal:
                            break
            except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
                print(f"    broad search failed: {exc}")
                failures += 1
        if count == 0:
            print("    No photos downloaded. Check internet access and run the script again later.")
        elif count < goal:
            print(f"    Got {count} photo(s); some Commons searches may have returned fewer usable images.")
        time.sleep(0.4)
    print("\nFinished. See photo_credits.csv for photo pages, authors and license labels.")
    if failures:
        print(f"Some searches failed ({failures}). You can run this script again; existing photos are preserved.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nStopped by user. Run again to continue; already downloaded photos remain in place.")
        raise SystemExit(130)
