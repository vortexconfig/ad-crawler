from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import json
import time

# === Setup ===

keywords = [
    "Ads", "GoogleAds", "Google", "Squarespace", "Wix", "GoDaddy", "Web", "site", "website", "web design", "web development",
    "UI/UX", "frontend", "backend", "WordPress", "Shopify", "Webflow", "Weebly", "SEO", "SEM", "PPC", "social media", "keyword",
    "ecommerce", "online store", "payment gateway", "cart", "app", "API", "database", "CMS", "custom code", "freelance",
    "developer", "designer", "build", "fix", "update", "Django", "React", "jQuery", "Next.js", "Node.js", "Vue.js", "Angular",
    "Express", "Flask", "Laravel", "Ruby on Rails", "JavaScript", "Python", "PHP", "HTML", "CSS", "Bootstrap", "Tailwind",
    "GraphQL", "REST", "AI integration", "machine learning", "chatbot", "vector database", "programmer", "coding", "redesign",
    "maintenance", "migrate", "online marketing", "digital marketing", "brand promotion", "marketing campaign",
    "content marketing", "email marketing", "lead generation", "funnel", "portal", "dashboard", "custom feature", "workflow",
    "booking system", "membership", "intranet", "file management", "documentation", "knowledgebase", "file upload", "data entry",
    "form builder", "automation", "integration", "bespoke", "custom solution", "prototype", "consulting"
]

keyword_regex = re.compile(r'\b(?:' + '|'.join(re.escape(k) for k in keywords) + r')\b', re.IGNORECASE)

# Add blacklist keywords
blacklist_keywords = [
    "Work from home",
    "Call today",
    "SiS4",
    "Earn",
    "Female",
    "Commission",
    "Feedback",
    "Clinical",
    "Research",
    "Study",
    "Survey",
    "Interview",
    "Focus Group",
    "Tester",
    "earn",
    "evaluate",
    "evaluator",
    "join",
    "reviewer",
    "mystery",
    "promotion",
    "coordinator",
    "focus",
    "jury",
    "fiasco",
    "reddit",
]

# Create blacklist regex pattern
blacklist_regex = re.compile(r'\b(?:' + '|'.join(re.escape(k) for k in blacklist_keywords) + r')\b', re.IGNORECASE)

cities = [
  "https://jacksonville.craigslist.org",
]

# === Selenium setup ===

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

def classify_location(text):
    text = text.lower()
    if "no remote" in text or "on-site" in text or "local only" in text:
        return "local"
    elif "remote" in text or "work from home" in text:
        return "remote"
    return "unspecified"

def crawl_city(city_url):
    results = {}
    gigs_url = f"{city_url}/search/cpg?search_radius=1000&search_distance=1000"

    print(f"Visiting {gigs_url}")
    driver.get(gigs_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Updated selector for listings
    listings = soup.select(".result-info")

    print(f"Found {len(listings)} listings in {city_url}")

    for listing in listings:
        a_tag = listing.select_one("a.posting-title")
        time_el = listing.select_one("div.meta").select_one("span")

        if not a_tag or not time_el:
            continue

        title = a_tag.text.strip()
        url = a_tag["href"]
        date = time_el["title"]

        # Skip if title contains blacklisted keywords
        if blacklist_regex.search(title):
            print(f"Skipping {title}")
            continue

        try:
            driver.get(url)
            time.sleep(2)
            post_soup = BeautifulSoup(driver.page_source, 'html.parser')
            body = post_soup.select_one("#postingbody")
            if body and keyword_regex.search(body.text):
                location_type = classify_location(body.text)
                results[title] = {
                    "title": title,
                    "url": url,
                    "datetime": date,
                    "location_type": location_type
                }
        except Exception as e:
            print(f"Failed to parse {url}: {e}")

        print(f"Finished processing listing {title}")

        # Wait for 2 seconds to prevent bot from being blocked
        time.sleep(2)

    return results

# === Run ===

all_results = {}
for city in cities:
    city_results = crawl_city(city)
    all_results.update(city_results)
    time.sleep(5)

with open("craigslist_gigs_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

driver.quit()
print(f"✅ Done! {len(all_results)} matching gigs saved.")
