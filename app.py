import streamlit as st
import json
from scraper.webscraper import WebScraper

st.title("CA.gov Agency & Services Scraper")

if st.button("Run Scraper"):
    with st.spinner("Scraping CA.gov services and agencies..."):
        scraper = WebScraper()
        services = scraper.get_services()
        agencies = {}
        for svc in services:
            agency_info = scraper.get_service_agency(svc['service_url'])
            agency_name = agency_info.get('agency_name', '').strip()
            agency_url = agency_info.get('agency_url', '').strip()
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
        agency_list = list(agencies.values())
        st.success(f"Scraped {len(agency_list)} agencies.")
        st.write(agency_list)
        st.download_button(
            label="Download JSON",
            data=json.dumps(agency_list, ensure_ascii=False, indent=2),
            file_name="agency_services.json",
            mime="application/json"
        )
else:
    st.info("Click 'Run Scraper' to begin scraping CA.gov services and agencies.")
