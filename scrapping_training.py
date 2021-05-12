# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt 
import pandas as pd


# # Set the executable path/Set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):

# # Assign the URL

# Visit the mars nasa news site

    url= 'https://redplanetscience.com'
    browser.visit(url)

# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


# # Set the HTML parse
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')


    slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    return news_title, news_p


# # Featured Images
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Mars Fact

#to scrapp the whole table, we will import it in a pandas table

#create a new dataframe from the html table. the index [0] is to tell pandas to pull the first
#table it encounters
df = pd.read_html('https://galaxyfacts-mars.com')[0]

#Assign columns to the new DataFrame
df.columns=['description', 'Mars', 'Earth']

#Set the description as the index. inplace=true means that the updated index will remain in place
df.set_index('description', inplace=True)
df


# # To convert the DataFrame back to HTML ready

df.to_html()


# # To end the automated browsing session 

#browser.quit()
   






