# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

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
    # Visit the mars nasa news site
        url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
        browser.visit(url)

    # Optional delay for loading the page
        browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
        html = browser.html
        news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    try:
    # Visit URL
        url = 'https://x.com/konstructivizm/status/1903452858156044659/photo/1'
        browser.visit(url)

    # Find and click the full image button
        full_image_elem = browser.find_by_tag('button')[1]
        full_image_elem.click()

    # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
         # Use the base url to create an absolute url
        img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    except AttributeError:
        return None
 
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")



    # If running as script, print scraped data
             
    #add the new function that will scrape the hemisphere data
def hemisphere_url(browser):
        url = 'https://science.nasa.gov/mars/facts/'
        browser.visit(url)
        #create the list 
        hemisphere_image_urls = [ ] 
        hemisphere_url= {}    
        for i in range(0,4):
            hemisphere_url= {}
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
        return hemisphere_image_urls
if __name__ == "__main__":
    print(scrape_all())