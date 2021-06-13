# Import Dependencies

import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

# Setting up Splinter

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


## Scrap Mars Site - Retrieve Recent News

# Defining url and visiting link for Mars (https://redplanetscience.com/)
url = 'https://redplanetscience.com/'
browser.visit(url)

# Creating beautifulsoup on webpage
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# Scrapping latest news title and paragraph text
news_title = soup.find('div', class_='content_title').text
news_p = soup.find('div', class_='article_teaser_body').text


## JPL Mars Space Images - Featured Image

# Defining url and visiting link
url = 'https://spaceimages-mars.com/'
browser.visit(url)

# Creating beautifulsoup on webpage
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# Scrapping featured_image_url, added url to relative path
featured_image_url = url + soup.find('img', class_='headerimage')['src']


## Mars Facts

# Defining url
url = 'https://galaxyfacts-mars.com/'

# Use Pandas to scrape tabular data from a page
mars_facts = pd.read_html(url)
mars_facts

# Convert into a Data Frame the Mars Comparison [0]
mars_compare_df = mars_facts[0]

# Skip the firs row
mars_compare_df= mars_compare_df[1:]

# Rename the columns
mars_compare_df.columns = ["Mars - Earth Comparison","Mars","Earth"]

# Set index to Description
mars_compare_df.set_index ("Mars - Earth Comparison", inplace=True)

# Print Dara Frame
mars_compare_df

# Convert into a Data Frame the Mars Fact [1]
mars_fact_df = mars_facts[1]

# Rename the columns
mars_fact_df.columns = ["Descripition","Values"]

# # Set index to Description
mars_fact_df.set_index ("Descripition", inplace=True)

# Print Dara Frame
mars_fact_df

# Save html code to folder Assets
html_table = mars_fact_df.to_html()

# Strip unwanted newlines to clean up the table
html_table.replace("\n", '')

# Save html code
mars_fact_df.to_html("html_table")


## Mars Hemispheres

# Defining url and visiting link
url = "https://marshemispheres.com/"
browser.visit(url)

# Creating beautifulsoup on webpage
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# Create an empty list to find and save all the image links
hemispheres_info = []

# Loop through the list of all hemispheres information

hemispheres = soup.find_all("div", class_="item")
hemispheres_url = "https://marshemispheres.com/"

for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    hemispheres_img = hemisphere.find("a", class_="itemLink product-item")["href"]
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_url + hemispheres_img)
    
    # HTML Object
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    # Create full image url
    img_url = hemispheres_url + soup.find("img", class_="wide-image")["src"]

	hemispheres_info.append({"title" : title, "img_url" : img_url})
    
 # Close the browser after scraping
 browser.quit()

 mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_fact_df': html_table,
        'hemispheres_info': hemispheres_info
    }

 # Return results
    return mars_data