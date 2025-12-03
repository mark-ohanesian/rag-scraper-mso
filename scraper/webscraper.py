import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebScraper:
    def get_all_departments(self) -> Dict[str, str]:
        """
        Scrape all CA department names and URLs from https://www.ca.gov/departments/all/
        Returns a dict: {name: url}
        """
        url = "https://www.ca.gov/departments/all/"
        resp = requests.get(url, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        departments = {}
        for a in soup.select('a'):
            href = a.get('href', '')
            name = a.get_text(strip=True)
            # Only include valid department links
            if href.startswith('http') and name:
                departments[name] = href
        return departments
    """
    Scrapes department names and URLs from CA.gov topics pages.
    Extendable for other sites and structures.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_topic_links(self) -> List[str]:
        resp = requests.get(self.base_url, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Find all topic links that are direct children of /topics/
        links = []
        for a in soup.select('a'):
            href = a.get('href', '')
            # Only include links like /topics/assistance/ (not /topics/topics/assistance/)
            if href.startswith('/topics/') and href.count('/') == 3:
                # Use absolute URLs from the page if available
                if href.startswith('http'):
                    links.append(href)
                else:
                    links.append(f"https://www.ca.gov{href}")
        # Remove duplicates and ensure valid URLs
        return sorted(set(links))

    def get_departments(self, topic_url: str) -> List[Dict[str, str]]:
        resp = requests.get(topic_url, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        all_depts = self.get_all_departments()
        departments = []
        # Look for service blocks: anchor followed by 'by Department ...' or similar
        for a in soup.select('a'):
            href = a.get('href', '')
            if href.startswith('http') and '/departments/' in href:
                # Find the next sibling or nearby text containing department info
                dept_name = None
                next_sib = a.find_next_sibling(text=True)
                if next_sib and 'by ' in next_sib:
                    dept_name = next_sib.strip().replace('by ', '')
                if not dept_name:
                    parent = a.parent
                    if parent:
                        texts = parent.stripped_strings
                        for t in texts:
                            if t != a.get_text(strip=True) and 'by ' in t:
                                dept_name = t.replace('by ', '').strip()
                                break
                if not dept_name:
                    dept_name = a.get_text(strip=True)
                # Debug print: show extracted department name
                print(f"Extracted department name: '{dept_name}' from href: {href}")
                # Try to match department name to official list
                matched_url = None
                for official_name, official_url in all_depts.items():
                    if dept_name.lower() in official_name.lower():
                        matched_url = official_url
                        print(f"Matched '{dept_name}' to official department: '{official_name}' -> {official_url}")
                        break
                if not matched_url:
                    print(f"No match found for '{dept_name}', using href: {href}")
                departments.append({'name': dept_name, 'url': matched_url or href})
        return departments

if __name__ == '__main__':
    scraper = WebScraper('https://www.ca.gov/topics/')
    topics = scraper.get_topic_links()
    for topic in topics:
        print(f"Scraping: {topic}")
        depts = scraper.get_departments(topic)
        for dept in depts:
            print(dept)
