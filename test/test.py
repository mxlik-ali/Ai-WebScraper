# import argparse
# import requests
# import os
# from urllib.parse import urlparse
# from collections import defaultdict
# from bs4 import BeautifulSoup
# import json

# parser = argparse.ArgumentParser()
# parser.add_argument("--site", type=str, required=True)
# parser.add_argument("--depth", type=int, default=3)


# def cleanUrl(url: str):
#     return url.replace("https://", "").replace("/", "-").replace(".", "_")


# def get_response_and_save(url: str):
#     response = requests.get(url)
#     if not os.path.exists("./scrape"):
#         os.mkdir("./scrape")
#     parsedUrl = cleanUrl(url)
#     with open("./scrape/" + parsedUrl + ".html", "wb") as f:
#         f.write(response.content)
#     return response


# def scrape_links(
#     scheme: str,
#     origin: str,
#     path: str,
#     depth=3,
#     sitemap: dict = defaultdict(lambda: ""),
# ):
#     siteUrl = scheme + "://" + origin + path
#     cleanedUrl = cleanUrl(siteUrl)

#     if depth < 0:
#         return
#     if sitemap[cleanedUrl] != "":
#         return

#     sitemap[cleanedUrl] = siteUrl
#     response = get_response_and_save(siteUrl)
#     soup = BeautifulSoup(response.content, "html.parser")
#     links = soup.find_all("a")

#     for link in links:
#         href = urlparse(link.get("href"))
#         if (href.netloc != origin and href.netloc != "") or (
#             href.scheme != "" and href.scheme != "https"
#         ):
#             continue
#         scrape_links(
#             href.scheme or "https",
#             href.netloc or origin,
#             href.path,
#             depth=depth - 1,
#             sitemap=sitemap,
#         )
#     return sitemap


# if __name__ == "__main__":
#     args = parser.parse_args()
#     url = urlparse(args.site)
#     sitemap = scrape_links(url.scheme, url.netloc, url.path, depth=args.depth)
#     with open("sitemap.json", "w") as f:
#         f.write(json.dumps(sitemap))
import requests
from bs4 import BeautifulSoup
import json

# Base URL and headers
base_url = 'https://www.scrapethissite.com/pages/ajax-javascript'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# Years to scrape
years = ['#2015', '#2014', '#2013', '#2012', '#2011', '#2010']

# Initialize a list to store the data
all_data = []

# Function to fetch and parse data for a given year
def fetch_films_for_year(year,headers):
    # AJAX request to fetch films for the specific year
    response = requests.get('https://www.scrapethissite.com/pages/ajax-javascript/#2015')
    print(response.status_code)
    response.raise_for_status()
    print(response)
   

    # Parse the HTML response
    # soup = BeautifulSoup(response.text, 'html.parser')
    with open('./scrape/www_scrapethissite_com-pages-ajax-javascript-.html','r') as f:
        soup = f.read()
    table_element = soup.find('table', class_='table')

    print(table_element)
    tbody_element = table_element.find('tbody')
    print(tbody_element)

    if table_element:
        # Extract data from the table
        print('table_element is present')
        table = []
        headers = [header.text.strip() for header in table_element.find_all('th')]
        print(headers)
        print(tbody_.find_all('tr'))
        for row in tbody_element.find_all('tr'):
            print('rows found')
            cells = row.find_all(['th', 'td'])
            values = [cell.text.strip() for cell in cells]
            film_data = dict(zip(headers, values))
            table.append(film_data)
        print(table)
        return table
                
    return []

# Loop through each year and fetch data
for year in years:
    films = fetch_films_for_year(year,headers)
    all_data.append({
        'year': year,
        'films': films
    })

# Save the data to a JSON file
with open('oscar_winning_films.json', 'w') as f:
    json.dump(all_data, f, indent=4)

print("Data saved to oscar_winning_films.json")
