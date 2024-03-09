import requests
from bs4 import BeautifulSoup

def scrape_internshala(keyword, num_pages=1):
    job_results = []
    for page in range(1, num_pages+1):
        url = f"https://internshala.com/internships/{keyword.lower()}-internship/page-{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        job_listings = soup.find_all('div', class_='individual_internship')
        
        for job in job_listings:
            try:
                internship_id = job['id'].split('_')[-1]
                title_tag = job.find('a', class_='view_detail_button')
                title = title_tag.text.strip()
                job_link = title_tag['href']
                company = job.find('div', class_='company').text.strip()
                location = job.find('a', class_='location_link').text.strip()
                job_results.append({
                    "id":internship_id,
                    "title":title,
                    "job_link":f"https://internshala.com/{job_link}",
                    "company":company,
                    "location":location
                })
            except AttributeError as e:
                print({'error': str(e)})
    return job_results

def scrape_job_data(keywords):
    scraped_job_results = []
    for keyword in keywords:
        print(f"Scraping job postings for {keyword}...")
        response = scrape_internshala(keyword,2)
        scraped_job_results.extend(response)
    
    return scraped_job_results
