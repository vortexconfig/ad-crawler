# Craigslist Web Crawler

This Python script uses **Selenium** and **BeautifulSoup** to crawl the **Computer Gigs** section of Craigslist in selected U.S. cities. It searches for listings related to web development, design, SEO, ecommerce, and other relevant services.

## 🔧 Features

- Searches major cities like New York, LA, and Chicago
- Detects keywords across web development, marketing, and tech
- Categorizes listings as **local**, **remote**, or **unspecified**
- Uses Selenium to render JavaScript pages
- Outputs results to `craigslist_gigs_results.json`

---

## 📦 Requirements

- Python 3.8+
- Google Chrome installed
- ChromeDriver installed and accessible from your PATH

---

## 🛠 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/vortexconfig/ad-crawler.git
cd ad-crawler
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

- MacOS
  - `source venv/bin/activate`
- Windows (CMD)
  - `venv\Scripts\activate`
- Windows (PowerShell)
  - `.\venv\Scripts\Activate.ps1`

### 4. Install Dependencies

```bash
pip3 install -r requirements.txt
```

## How to Run the Script

```bash
python craigslist_crawler.py
```

This will:

- Open Craigslist in a headless browser
- Crawl the Computer Gigs section of Craigslist in selected cities
- Search for listings containing specific tech keywords
- Save the results in craigslist_gigs_results.json

## Output Format

```json
{
  "title": "Looking for WordPress Developer",
  "url": "https://losangeles.craigslist.org/cpg/abc123.html",
  "datetime": "2025-05-16 10:45",
  "location_type": "remote"
}
```
