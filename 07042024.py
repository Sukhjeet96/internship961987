#!/usr/bin/env python
# coding: utf-8

# In[12]:


import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_most-viewed_YouTube_videos"

try:
    response = requests.get(url)
    response.raise_for_status()  

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', class_='wikitable sortable')

    ranks = []
    names = []
    artists = []
    upload_dates = []
    views = []

    for row in table.find_all('tr')[1:]:  
        cells = row.find_all('td')
        ranks.append(cells[0].text.strip())
        names.append(cells[1].text.strip())
        artists.append(cells[2].text.strip())
        upload_dates.append(cells[3].text.strip())
        views.append(cells[4].text.strip())

    for i in range(len(ranks)):
        print("Rank:", ranks[i])
        print("Name:", names[i])
        print("Artist:", artists[i])
        print("Upload Date:", upload_dates[i])
        print("Views:", views[i])
        print("\n")

except requests.exceptions.RequestException as e:
    print("Error fetching the webpage:", e)
except Exception as e:
    print("An error occurred:", e)


# In[22]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_datasets_from_uci():
    url = "https://archive.ics.uci.edu/"
    show_all_datasets_url = "https://archive.ics.uci.edu/ml/datasets.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }


    response = requests.get(show_all_datasets_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        datasets_table = soup.find("table", class_="table")
        dataset_rows = datasets_table.find_all("tr")[1:] 
        datasets_data = []

        for row in dataset_rows:
            columns = row.find_all("td")
            dataset_name = columns[0].text.strip()
            data_type = columns[1].text.strip()
            task = columns[2].text.strip()
            attribute_type = columns[3].text.strip()
            num_instances = columns[4].text.strip()
            num_attributes = columns[5].text.strip()
            year = columns[6].text.strip()

            datasets_data.append({
                "Dataset Name": dataset_name,
                "Data Type": data_type,
                "Task": task,
                "Attribute Type": attribute_type,
                "No of Instances": num_instances,
                "No of Attributes": num_attributes,
                "Year": year
            })

        return datasets_data
    else:
        print("Failed to retrieve data from the website.")
        return []

def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("datasets_from_uci.csv", index=False)
    print("Data saved to CSV successfully.")

if __name__ == "__main__":
    datasets_data = scrape_datasets_from_uci()
    if datasets_data:
        save_to_csv(datasets_data)


# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def scrape_billboard_top_100():
    driver = webdriver.Chrome(executable_path="chromedriver.exe") 
    driver.maximize_window()

    driver.get("https://www.billboard.com/")
    
    charts_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Charts")))
    charts_option.click()

    hot_100_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Hot 100")))
    hot_100_link.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".chart-list")))


    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")
    chart_list = soup.find("ol", class_="chart-list__elements")

    songs_data = []
    for song in chart_list.find_all("li", class_="chart-list__element"):
        song_details = {}
        song_details["Song Name"] = song.find("span", class_="chart-element__information__song").text.strip()
        song_details["Artist Name"] = song.find("span", class_="chart-element__information__artist").text.strip()
        song_details["Last Week Rank"] = song.find("span", class_="chart-element__meta text--center color--secondary text--last").text.strip() if song.find("span", class_="chart-element__meta text--center color--secondary text--last") else "-"
        song_details["Peak Rank"] = song.find("span", class_="chart-element__meta text--center color--secondary text--peak").text.strip()
        song_details["Weeks on Board"] = song.find("span", class_="chart-element__meta text--center color--secondary text--week").text.strip()
        songs_data.append(song_details)

    return songs_data

def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("billboard_top_100.csv", index=False)
    print("Data saved to CSV successfully.")

if __name__ == "__main__":
    top_100_data = scrape_billboard_top_100()
    if top_100_data:
        save_to_csv(top_100_data)


# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_highest_selling_novels():
    url = "https://www.theguardian.com/news/datablog/2012/aug/09/best-selling-books-all-time-fifty-shades-grey-compare"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        novels_data = []
        
        table = soup.find("table")
        rows = table.find_all("tr")[1:] 

        for row in rows:
            columns = row.find_all("td")
            book_name = columns[0].text.strip()
            author_name = columns[1].text.strip()
            volumes_sold = columns[2].text.strip()
            publisher = columns[3].text.strip()
            genre = columns[4].text.strip()

            novels_data.append({
                "Book Name": book_name,
                "Author Name": author_name,
                "Volumes Sold": volumes_sold,
                "Publisher": publisher,
                "Genre": genre
            })

        return novels_data
    else:
        print("Failed to retrieve data from the website.")
        return []

def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("highest_selling_novels.csv", index=False)
    print("Data saved to CSV successfully.")

if __name__ == "__main__":
    novels_data = scrape_highest_selling_novels()
    if novels_data:
        save_to_csv(novels_data)


# In[ ]:


import requests
from bs4 import BeautifulSoup

url = "https://www.bcci.tv/"

try:
    response = requests.get(url)
    response.raise_for_status()  


    soup = BeautifulSoup(response.text, 'html.parser')

    fixtures_link = soup.find('a', text='International Fixtures')['href']
    fixtures_url = url + fixtures_link

    fixtures_response = requests.get(fixtures_url)
    fixtures_response.raise_for_status()  

    fixtures_soup = BeautifulSoup(fixtures_response.text, 'html.parser')

    fixtures = fixtures_soup.find_all('div', class_='fixture__format-strip')

    for fixture in fixtures:
        series = fixture.find('span', class_='u-unskewed-text').text.strip()
        place = fixture.find('p', class_='fixture__additional-info').text.strip()
        date = fixture.find('span', class_='fixture__datetime tablet-only').text.strip()
        time = fixture.find('span', class_='fixture__time').text.strip()

        print("Series:", series)
        print("Place:", place)
        print("Date:", date)
        print("Time:", time)
        print("\n")

except requests.exceptions.RequestException as e:
    print("Error fetching the webpage:", e)
except Exception as e:
    print("An error occurred:", e)


# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def initialize_driver():
   
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    driver_path = "chromedriver.exe"  
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

url = "https://github.com/"

try:
    driver = initialize_driver()

    driver.get(url)

    explore_dropdown = driver.find_element(By.XPATH, "//summary[contains(text(), 'Explore')]")
    explore_dropdown.click()


    trending_option = driver.find_element(By.XPATH, "//a[contains(text(), 'Trending')]")
    trending_option.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Box-row")))

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    repositories = soup.find_all('article', class_='Box-row')

      for repo in repositories:
        repo_title = repo.find('h1', class_='h3 lh-condensed').text.strip()
        repo_description = repo.find('p', class_='col-9 color-text-secondary my-1 pr-4').text.strip()
        contributors_count = repo.find('a', class_='Link--muted d-inline-block mr-3').text.strip()
        language_used = repo.find('span', itemprop='programmingLanguage').text.strip()

        print("Repository Title:", repo_title)
        print("Repository Description:", repo_description)
        print("Contributors Count:", contributors_count)
        print("Language Used:", language_used)
        print("\n")

except Exception as e:
    print("An error occurred:", e)
finally:
  
    driver.quit()


# In[ ]:


import requests
from bs4 import BeautifulSoup

url = "http://statisticstimes.com/"

try:
    response = requests.get(url)
    response.raise_for_status() 

    soup = BeautifulSoup(response.text, 'html.parser')

    economy_link = soup.find('a', text='Economy')['href']
    economy_url = url + economy_link

    economy_response = requests.get(economy_url)
    economy_response.raise_for_status()

    economy_soup = BeautifulSoup(economy_response.text, 'html.parser')

    india_gdp_link = economy_soup.find('a', text='India GDP')['href']
    india_gdp_url = url + india_gdp_link

 
    india_gdp_response = requests.get(india_gdp_url)
    india_gdp_response.raise_for_status()  

    india_gdp_soup = BeautifulSoup(india_gdp_response.text, 'html.parser')
    
    gdp_table = india_gdp_soup.find('table', class_='display dataTable')

    for row in gdp_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        rank = columns[0].text.strip()
        state = columns[1].text.strip()
        gdp_18_19 = columns[2].text.strip()
        gdp_19_20 = columns[3].text.strip()
        share_18_19 = columns[4].text.strip()
        gdp_billion = columns[5].text.strip()

        print("Rank:", rank)
        print("State:", state)
        print("GSDP(18-19):", gdp_18_19)
        print("GSDP(19-20):", gdp_19_20)
        print("Share(18-19):", share_18_19)
        print("GDP($ billion):", gdp_billion)
        print("\n")

except requests.exceptions.RequestException as e:
    print("Error fetching the webpage:", e)
except Exception as e:
    print("An error occurred:", e)


# In[ ]:





# In[ ]:





# In[ ]:




