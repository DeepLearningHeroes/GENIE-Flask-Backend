import requests
import pickle
from bs4 import BeautifulSoup
from utils import text_cleaner
from utils.model_support import skill_finder

def scrape_individual_job_internshala(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        spans = soup.find_all('span', class_='round_tabs')
        keywords = []
        for span in spans:
          text = span.text
          keywords.append(text.strip())
        
        return keywords
    except Exception as error:
        print(error)

def scrape_internshala(model,keyword, num_pages=1):
    job_results = []
    for page in range(1, num_pages+1):
        url = f"https://internshala.com/internships/{keyword.lower()}-internship/page-{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        job_listings = soup.find_all('div', class_='individual_internship')
        heading = soup.find_all('h1',class_="active-header")
        print(heading)
        #todo - write logic to handle heading to check if a skill's page exists on internshala or not

        for job in job_listings:
            try:
                internship_id = job['id'].split('_')[-1]
                title_tag = job.find('a', class_='view_detail_button')
                title = title_tag.text.strip()
                job_link = title_tag['href']
                company = job.find('div', class_='company').text.strip()
                location = job.find('a', class_='location_link').text.strip()
                
                keywords = scrape_individual_job_internshala(f"https://internshala.com{job_link}")
                final_keywords=[]
                for _keyword in keywords:
                    res = skill_finder(model,_keyword)
                    if len(res)>0:
                        final_keywords.extend(res)

                if len(final_keywords) == 0:
                    final_keywords.extend(keyword)
                job_results.append({
                    "id":internship_id,
                    "title":title,
                    "job_link":f"https://internshala.com{job_link}",
                    "company":text_cleaner.cleanText(company.split(title)[1]).strip(),
                    "location":location,
                    "keywords":final_keywords
                })
            except AttributeError as e:
                print({'error': str(e)})
    return job_results

def scrape_job_data(model,keywords=['javascript','python','c++']):
    try:
        scraped_job_results = []
        for keyword in keywords:
            print(f"Scraping job postings for {keyword}...")
            response = scrape_internshala(model,keyword,1)
            scraped_job_results.extend(response)
    
        return scraped_job_results
    except Exception as error:
        print(f'Error: {error}')
        return error
   
