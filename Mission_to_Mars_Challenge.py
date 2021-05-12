#!/usr/bin/env python
# coding: utf-8

# In[16]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# # Set the executable path

# In[17]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# # Assign the URL

# In[18]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# # Set the HTML parser

# In[19]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[20]:


slide_elem.find('div', class=_'content_title')


# In[21]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[22]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # Featured Images

# In[23]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[24]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[25]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[26]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[27]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Mars Fact

# In[28]:


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

# In[29]:


df.to_html()


# # To end the automated browsing session 

# In[30]:


#browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# # Hemispheres

# In[31]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[41]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(0,4):
    hemisphere_url = {}
    browser.find_by_css('a.product-item h3')[i].click()
    #find the sample image
    element = browser.links.find_by_text('Sample').first
    #full resolution image url
    img_url = element['href']
    #image title
    title = browser.find_by_css("h2.title").text
    #add the dictionary with the image url string and hemisphere image title to the list
    hemisphere_url["img_url"] = img_url
    hemisphere_url["title"] = title
    hemisphere_image_urls.append(hemisphere_url)
    browser.back()


# In[42]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[43]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




