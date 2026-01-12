from scraper.webscraper import WebScraper
from rag.pipeline import RAGPipeline
import os
import json

def main():
    # Scrape all services and their agencies
    scraper = WebScraper()
    services = scraper.get_services()
    print(f"Found {len(services)} services.")
    # Build agency-centric data structure
    agencies = {}
    for i, svc in enumerate(services):
        print(f"[{i+1}/{len(services)}] Scraping agency for: {svc['service_name']} ({svc['service_url']})")
        agency_info = scraper.get_service_agency(svc['service_url'])
        agency_name = agency_info.get('agency_name', '').strip()
        agency_url = agency_info.get('agency_url', '').strip()
        print(f"  -> Extracted agency: '{agency_name}' | URL: '{agency_url}'")
        if not agency_name:
            continue
        key = (agency_name, agency_url)
        if key not in agencies:
            agencies[key] = {
                'agency_name': agency_name,
                'agency_url': agency_url,
                'services': []
            }
        agencies[key]['services'].append(svc['service_name'])
    # Convert to list for JSON output
    agency_list = list(agencies.values())
    print(f"Writing {len(agency_list)} agencies to data/agency_services.json")
    os.makedirs('data', exist_ok=True)
    try:
        with open('data/agency_services.json', 'w', encoding='utf-8') as f:
            json.dump(agency_list, f, ensure_ascii=False, indent=2)
        print("Write successful.")
    except Exception as e:
        print(f"Error writing agency_services.json: {e}")

if __name__ == "__main__":
    main()
