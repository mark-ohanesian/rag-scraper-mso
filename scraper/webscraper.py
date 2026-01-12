
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebScraper:
    """
    Scrapes all service names and links from https://www.ca.gov/services/list/.
    For each service, visits its page to extract agency name and agency URL.
    """
    def __init__(self):
        self.services_list_url = "https://www.ca.gov/services/list/"

    def get_services(self) -> List[Dict[str, str]]:
        resp = requests.get(self.services_list_url, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        services = []
        # Find the main filter list component
        filterlist = soup.find('cagovhome-filterlist')
        if not filterlist:
            print("No cagovhome-filterlist found on page.")
            return services
        # Find all <li data-row-key> inside the filterlist
        for li in filterlist.find_all('li', attrs={'data-row-key': True}):
            a = li.find('a', href=True)
            if not a:
                continue
            name = a.get_text(strip=True)
            href = a['href']
            # Only include valid service links
            if href.startswith('/'):
                full_url = f"https://www.ca.gov{href}"
            else:
                full_url = href
            services.append({'service_name': name, 'service_url': full_url})
        return services

    def get_service_agency(self, service_url: str) -> Dict[str, str]:
        resp = requests.get(service_url, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        agency_name = None
        agency_url = None
        dept_page_url = None
        # Look for <main id="main"> and <a> with department/agency name
        main = soup.find('main', id='main')
        if main:
            # Find department/agency link (relative, e.g. '../../')
            dept_link = None
            for a in main.find_all('a', href=True):
                if 'department' in a.get_text(strip=True).lower() or 'agency' in a.get_text(strip=True).lower():
                    dept_link = a
                    break
            if dept_link:
                agency_name = dept_link.get_text(strip=True)
                # Resolve department page URL
                dept_page_url = requests.compat.urljoin(service_url, dept_link['href'])
        # If we found a department page, fetch it to get the true agency URL
        if dept_page_url:
            try:
                dept_resp = requests.get(dept_page_url, verify=False)
                dept_resp.raise_for_status()
                dept_soup = BeautifulSoup(dept_resp.text, 'html.parser')
                dept_main = dept_soup.find('main', id='main')
                if dept_main:
                    btn = dept_main.find('a', class_='btn btn-primary btn-lg m-r-md m-b', href=True, string=lambda s: s and 'department website' in s.lower())
                    if btn:
                        agency_url = btn['href']
            except Exception as e:
                print(f"Error fetching department page {dept_page_url}: {e}")
        # Fallback: previous logic for external links
        if not agency_name:
            for a in soup.select('a'):
                href = a.get('href', '')
                text = a.get_text(strip=True)
                if href and not href.startswith('/services/') and not href.startswith('/topics/') and 'ca.gov' in href:
                    agency_name = text
                    agency_url = href
                    break
        # Fallback: look for agency name in text
        if not agency_name:
            for tag in soup.find_all(['h2', 'h3', 'span', 'div']):
                txt = tag.get_text(strip=True)
                if 'agency' in txt.lower() or 'department' in txt.lower():
                    agency_name = txt
                    break
        return {'agency_name': agency_name or '', 'agency_url': agency_url or ''}
