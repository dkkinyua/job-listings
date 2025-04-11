# A full ETL pipeline to scrape data, transform and load it into Excel sheets.
Have you ever needed up-to-date job listings but struggled to find one clean source? In this project, I built a full ETL (Extract, Transform, Load) pipeline using Python to scrape internship job data from websites, clean and process it, and load it into an Excel file for analysis or tracking.

This project is perfect for anyone interested in web scraping, data pipelines, or automating jobs and tasks with Python and cron!

The project's GitHub link is: [GitHub](https://github.com/dkkinyua/job-listings)

## What the Project Entails

The pipeline performs three main tasks:

1. **Extract**
   - Scrapes internship listings from [MyJobMag Kenya](https://www.myjobmag.co.ke/)
   - Applies filters like:
     - `q=Internship`
     - `location=Nairobi`
     - `&currentpage={page_number}`

2. **Transform**
   - Cleans the data using:
     - `BeautifulSoup` for HTML parsing
     - `pandas` for data manipulation
   - Tasks performed:
     - Removes malformed descriptions
     - Drops duplicate entries
     - Filters out rows with missing or invalid data

3. **Load**
   - Saves the cleaned data into an Excel file: `internships.xlsx`
   - Useful for:
     - Job search organization
     - Data analysis
     - Dashboards and reporting

## Step by Step Explanation.

### a. Extract.

Use `requests` to make GET requests to the website's server and `beautifulsoup4` to scrape content from the website.

Also, use `dotenv` to hide environmental variables like the website's URL.

To install these packages, run the following command in your terminal:

```bash

pip install beautifulsoup4 requests dotenv

```

Build a script that extracts the job's title, description, posted date, and link to follow when applying to the internship/job.

Import the necessary libraries required and initialize empty lists to contain the various column data.

```python

import os
import json
import requests
from dotenv import load_dotenv

internships = []
titles = []
descriptions = []
opened_dates = []
links = []

```


The request gets the content from the server by looping through the pages and passes it into the variable `soup`. Then, loop through the listings found by soup's `find_all()` which finds HTML elements by its class.

```python

def extract():
    for i in range(1, 6):
        url = f'{URL}&currentpage={i}'

        headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

        listings = soup.find_all('li', class_='job-list-li')

        for listing in listings:
            title = listing.find('h2')
            title_text = clean_text(title.get_text()) if title else 'N/A'
            titles.append(title_text)

            a_tag = listing.find('a')
            link = a_tag['href'] if a_tag and a_tag.has_attr('href') else 'N/A'
            job_links = f'https://myjobmag.co.ke{link}' if a_tag and a_tag.has_attr('href') else 'N/A'
            links.append(job_links)

            description = listing.find('li', class_='job-desc')
            description_text = clean_text(description.get_text()) if description else 'N/A'
            descriptions.append(description_text)

            opened_at = listing.find('li', id='job-date')
            opened_text = opened_at.get_text(strip=True) if opened_at else 'N/A'
            opened_dates.append(opened_text)

            time.sleep(response.elapsed.total_seconds())

```

**HINT: Using `time.sleep(response.elapsed.total_seconds())` is a good practice to use when sending requests to a server as it lets the request take some time before sending another request. This is respectful to do to avoid sending too many requests to the server at a time and prevents crashing.**

To clean this data collected from scraping, load the data into a JSON file using the `json` module.

```python

def load_data(list):
    with open('data.json', 'w') as f:
        json.dump(list, f, indent=4)

    print('Data loaded into JSON successfully')

```

To run this script:

```python

if __name__ == '__main__':
    extract()
    load_data(internships)

```

**HINT: Using this pattern `if __name__ == '__main__'` helps us to run our scripts within other scripts without encountering any errors and helps in testing our scripts elsewhere.**

### b. Transform/Clean.

The content collected from the website had some unwanted characters like Unicode representations e.g. \u2023

Create a function `clean_text` that cleans these characters off the content. *Check the extract() function at title and description.*

```python

def clean_text(text):
    if not text:
        return 'N/A'
    text = html.unescape(text)
    text = text.replace('\r', '').replace('\n', ' ').replace('\t', ' ').replace('\u00a0', ' ').replace('\u2019', ' ').replace('\u2023', ' ').replace('\u2013', ' ')
    text = ' '.join(text.split())
    return text.strip()

```

Use the `pandas` and `numpy` to build a script that cleans this data and loads it into an Excel sheet.

Load the data from JSON format into a Pandas dataframe:

```python

import pandas as pd
import numpy as np

df = pd.read_json('data.json')

```

When printing df, the columns' data is in a Python list, which we don't want it to be in. We need to explode the columns into rows and reset the index.


![Dataframe](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/71ws7bmp1mqnjbozo6m0.png)

```python

df = df.explode(['title', 'description', 'opened_on', 'link']).reset_index(drop=True)

```

The columns will be exploded. but the first row starts at index 0. To make the first row to have index = 1:

```python

df.index = df.index + 1

```

The data contains N/A in the rows which implies that these rows contain no relevant information and we need to drop these rows.

We need to replace the N/A values with `np.nan` values which will be easier to drop.

```python

df = df.replace('N/A', np.nan)
df.dropna(inplace=True)

```

Now, the data is clean and ready to be loaded into an Excel sheet.

### c. Load.

After transforming the data, Load the transformed data into an Excel sheet for better visualization and interaction with the end user.

Before loading the data into an Excel sheet, install `openpyxl` which is a Python package that helps with loading of dataframes into Excel sheets. To install:

```bash

pip install openpyxl

```

After installation, add the following line to add the data into an Excel sheet:

```python

df.to_excel('internships.xlsx')

```

## End result.

![Excel spreadsheet](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gg5ed2qka6uvllxgfyn2.png)


**As a student and job-seeker, I wanted to automate the process of checking for new internship listings. Building this ETL pipeline allowed me to:**
   - Learn scripting 
   - Building ETL pipelines using Python.
   - Cleaning and Manipulating data using `pandas` and `numpy`.
   - Automate manual tracking tasks

I'll automate these tasks to be scraping on weekdays at 9:30AM EAT (East African Time) and a script that sends me emails to inform me that data is available for use in Excel.

**ALERT: Some websites do not support scraping and it is wise to go through the company's Terms and Conditions or Policy to check if they have any problems with scraping. If so, look for an API to fetch data as this will prevent any legal measures taken against you.**

**Happy hacking <3**




