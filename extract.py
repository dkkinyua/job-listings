import json
import time
import requests
from bs4 import BeautifulSoup

internships = []
titles = []
descriptions = []
opened_dates = []
links = []

for i in range(1, 6):
    url = f'https://www.myjobmag.co.ke/search/jobs?q=Internship&location=Nairobi&location-sinput=Nairobi&currentpage={i}'

    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        listings = soup.find_all('li', class_='job-list-li')

        for listing in listings:
            title = listing.find('h2')
            title_text = title.get_text(strip=True) if title else 'N/A'
            titles.append(title_text)

            a_tag = listing.find('a')
            link = a_tag['href'] if a_tag and a_tag.has_attr('href') else 'N/A'
            job_links = f'https://myjobmag.co.ke{link}' if a_tag and a_tag.has_attr('href') else 'N/A'
            links.append(job_links)

            description = listing.find('li', class_='job-desc')
            description_text = description.get_text(strip=True) if description else 'N/A'
            descriptions.append(description_text)

            opened_at = listing.find('li', id='job-date')
            opened_text = opened_at.get_text(strip=True) if opened_at else 'N/A'
            opened_dates.append(opened_text)

            time.sleep(response.elapsed.total_seconds()) # call another request after the elapsed time for the previous request
    else:
        print(f'There is an error fetching data: {response.status_code}')

internships.append({
    'title': titles,
    'description': descriptions,
    'opened_on': opened_dates,
    'link': links
})

print(f'Append complete: {internships}')
# print(titles)
# print(opened_dates)
#print(f'Printed {len(opened_dates)} dates')
#print(f'Printed {len(titles)} titles')
#print(f'Printed {len(descriptions)} descriptions')
#print(f'Printed {len(links)} links')


    