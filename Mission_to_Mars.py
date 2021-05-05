#!/usr/bin/env python
# coding: utf-8

# In[14]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# # Set the executable path

# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# # Assign the URL

# In[4]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# # Set the HTML parser

# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[6]:


slide_elem.find('div', class=_'content_title')


# In[ ]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Mars Fact

# In[17]:


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

# In[18]:


df.to_html()


# # To end the automated browsing session 

# In[19]:


browser.quit()


# In[ ]:




