
# coding: utf-8

# In[38]:


# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import re
import time
import pandas as pd


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mars
collection = db.items

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_listings = {}
    # ## Scrape NASA News

    # URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Path to get titles of articles
    title = '//div[@class="content_title"]/a'
    #Reading the results  
    nasa_title = browser.find_by_xpath(title).first.text
    #Scrape teaser
    teaser = '//div[@class="article_teaser_body"]'
    nasa_teaser = browser.find_by_xpath(teaser).first.text

    #save listing
    mars_listings['nasa_title'] = nasa_title
    mars_listings['nasa_teaser'] = nasa_teaser

    # ## JPL Mars Space Images - Featured Image

    #JPL full-image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    browser.find_by_id('full_image').click()
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']
    
    mars_listings['featured_image_url'] = featured_image_url

    # ## Twitter Weather

    #Mars twitter
    twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter)
    for text in browser.find_by_css('.tweet-text'):
        if text.text.partition(' ')[0] == ', high':
            weather = text.text
            break
    mars_listings['weather'] = weather


    # ## Mars Facts
    # We visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet
    marsfacts = 'https://space-facts.com/mars/'
    tables = pd.read_html(marsfacts)
    tables


    # Now let's slice off the dataframe using normal indexing.
    df = tables[0]
    df.columns = ['Col1', 'Col2']
    df.set_index('Col1', inplace=True)
    #Converting the data to a HTML table string and stripping unwanted newlines to clean up the table

    mars_html = df.to_html()
    mars_html.replace("\n", " ")
    mars_listings['mars_html'] = mars_html

    # ## Mars Hemispheres
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_image_urls = []
    browser.visit(usgs_url)
    for i in range(4):
        dictionary = {}
        hemis = browser.find_by_tag('h3')[i].text
        browser.find_by_css('.thumb')[i].click()
        img = browser.find_by_text('Sample')['href']
        browser.back()
        dictionary['hemisphere'] = hemis
        dictionary['img'] = img
        hemisphere_image_urls.append(dictionary)
    
    mars_listings['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_listings


