import requests
from bs4 import BeautifulSoup

def scrape_internshala(keyword, num_pages=1):
    for page in range(1, num_pages+1):
        url = f"https://internshala.com/internships/{keyword.lower()}-internship/page-{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        job_listings = soup.find_all('div', class_='individual_internship')
        print(job_listings[0])

        for job in job_listings:
            title = job.find('div', class_='profile').text.strip()
            company = job.find('div', class_='company_name').text.strip()
            location = job.find('a', class_='location_link').text.strip()
            print(f"Internshala - {title} at {company} ({location})")

def scrape_job_data(keywords):

    for keyword in keywords:
        print(f"Scraping job postings for {keyword}...")
        scrape_internshala(keyword)
