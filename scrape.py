# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    service = Service(ChromeDriverManager().install())
    browser = Browser('chrome', service=service, headless=False)
    news_title, news_paragraph = mars_news(browser)
    hemisphere = hemisphere_url(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere": hemisphere
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    try:
        # Scrape Mars News
        url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
        browser.visit(url)
        browser.is_element_present_by_css('div.list_text', wait_time=1)

        html = browser.html
        news_soup = soup(html, 'html.parser')

        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    try:
        # Visit URL
        url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
        browser.visit(url)

        # Find and click the full image button
        browser.find_by_tag('button')[1].click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    except (AttributeError, IndexError):
        return None

    return img_url

def mars_facts():
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
        df.columns=['Description', 'Mars', 'Earth']
        df.set_index('Description', inplace=True)
    
    except (BaseException, IndexError):
        return None

    # Convert dataframe into HTML format, add bootstrap and link to custom CSS
    return df.to_html(classes="table table-striped mars-table")

def hemisphere_url(browser):
    try:
        url = 'https://marshemispheres.com/'
        browser.visit(url)
        hemisphere_image_urls = []

        # Loop through each link to get data
        for i in range(4):
            browser.find_by_css('a.product-item h3')[i].click()
            element = browser.links.find_by_text('Sample').first
            img_url = element['href']
            title = browser.find_by_css('h2.title').text
            hemisphere_image_urls.append({"img_url": img_url, "title": title})
            browser.back()
    
    except (AttributeError, IndexError):
        return []

    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())
