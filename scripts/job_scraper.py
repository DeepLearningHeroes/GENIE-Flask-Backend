import requests
import pickle
from bs4 import BeautifulSoup
from utils import text_cleaner
from utils.model_support import skill_finder

def scrape_individual_job_internshala(url):
    print(url)
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
        url = f"https://internshala.com/internships/{(keyword.lower())}-internship/page-{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        job_listings = soup.find_all('div', class_='individual_internship')
        heading = soup.find_all('h1',class_="active-header")
        for content in heading[0]:
            heading_title = content.split(" ")

        if heading_title[1] == "Total":
            break
        #todo - write logic to handle heading to check if a skill's page exists on internshala or not

        for job in job_listings:
            try:
                if job is None:
                    continue
                internship_id = job['id']
                if internship_id is None:
                    continue
                else:
                    internship_id = internship_id.split('_')[2]
                title = job.select_one('.heading_4_5')
                if title is None:
                    title = "Title"
                else:
                    title = title.text.strip()
                job_link = job.select_one('.view_detail_button_outline')
                if job_link is None:
                    job_link = "link"
                else:
                    job_link = job_link['href']
                company = job.select_one('.company_name p')
                if company is None:
                    continue
                company = company.text.strip()
                location = job.select_one('#location_names span a')
                if location is None:
                    continue
                location = location.text.strip()
                
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
                    "company":company,
                    "location":location,
                    "keywords":final_keywords
                })
            except AttributeError as e:
                print({'error': str(e)})
    return job_results

def scrape_job_data(model,keywords=['javascript','python','c++']):
    try:
        scraped_job_results = []
        visited = set()
        for keyword in keywords:
            print(f"Scraping job postings for {keyword}...")
            if text_cleaner.cleanText(keyword) in visited:
                print(f"Job postings for {keyword} already scraped...")
                continue
            
            else:
                visited.add(text_cleaner.cleanText(keyword))

            response = scrape_internshala(model,keyword,1)
            print(len(response))
            scraped_job_results.extend(response)
    
        return scraped_job_results
    except Exception as error:
        print(f'Error: {error}')
        return error
   
