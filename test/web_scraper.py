import requests
import json
from bs4 import BeautifulSoup

# Function to scrape and parse the Wikipedia page
def scrape_wikipedia_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Error fetching the Wikipedia page: {e}")
        return None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error parsing the Wikipedia page: {e}")
        return None

    # Define the data structure
    page_structure = {
        'intro': [],
        'sections': []
    }

    current_section = None
    current_subsection = None

    try:
        for element in soup.find_all(['h1','h2', 'h3', 'p', 'table', 'img','li']):
            if element.name == 'h1':
                current_section = {
                    'title': element.get_text(strip=True),
                    'subsections': [],
                    'content': [],
                    'tables': [],
                    'images': []
                }
                page_structure['sections'].append(current_section)
                current_subsection = None
            elif element.name == 'h3' and current_section:
                current_subsection = {
                    'title': element.get_text(strip=True),
                    'content': [],
                    'tables': [],
                    'images': []
                }
                current_section['subsections'].append(current_subsection)
            elif element.name == 'p' or element.name == 'li':
                content = element.get_text(strip=True)
                if current_subsection:
                    current_subsection['content'].append(content)
                elif current_section:
                    current_section['content'].append(content)
                else:
                    page_structure['intro'] += content + "\n"
            elif element.name == 'table':
                table = []
                headers = []
                for row in element.find_all('tr'):
                    cells = row.find_all(['th', 'td'])
                    if not headers and all(cell.name == 'th' for cell in cells):
                        headers = [cell.get_text(strip=True) for cell in cells]
                    else:
                        values = [cell.get_text(strip=True) for cell in cells]
                        if len(values) == len(headers):
                            table.append(dict(zip(headers, values)))
                
                table_entry = {'headers': headers, 'rows': table}
                if current_subsection:
                    current_subsection['tables'].append(table_entry)
                elif current_section:
                    current_section['tables'].append(table_entry)
                else:
                    page_structure['intro'] += str(table_entry) + "\n"
            elif element.name == 'img':
                img_url = element.get('src')
                if current_subsection:
                    current_subsection['images'].append(img_url)
                elif current_section:
                    current_section['images'].append(img_url)
                else:
                    continue
    except Exception as e:
        print(f"Error processing the HTML content: {e}")
        return None
    with open("web_scraped_content.json", "w") as f:
        f.write(json.dumps(page_structure))
    return page_structure

scrape_wikipedia_page('https://www.scrapethissite.com/pages/ajax-javascript/#2015')