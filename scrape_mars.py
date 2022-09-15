#code from jupyter notebook
#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup 
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# NASA Mars News-website scraping
def scrape_news():
   
    #setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
   
    #website
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)

    #html to soup obj
    news_web = browser.html
    news_obj = BeautifulSoup(news_web, 'html.parser')
    browser.quit()

    #find title/text from news
    news_texts = news_obj.find_all('div', class_='list_text')
    latest_news = news_texts[0]
    news_title = latest_news.find('div', class_='content_title').text
    news_p = latest_news.find('div', class_='article_teaser_body').text

    return (news_title, news_p)

# JPL Mars Space Images:Featured Image-Web Scraping
def scrape_featured_image():
   
    #setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
   
    #website
    image_url = 'https://spaceimages-mars.com'
    browser.visit(image_url)

    #html to soup obj
    image_web = browser.html
    image_obj = BeautifulSoup(image_web, 'html.parser')
    browser.quit()

    #find images
    image_srcs = image_obj.find_all('div', class_='floating_text_area')

    #loop
    for image_src in image_srcs:
       
        try:
            image_filename = image_src.a['href']
            featured_image_url = f"{image_url}/{image_filename}"
        except AttributeError as e:
            print(e)

    return featured_image_url

   
# Mars Facts-Web Scraping
def scrape_facts():
   
    #setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #website
    facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(facts_url)

    #html to soup obj
    facts_web = browser.html
    facts_obj = BeautifulSoup(facts_web, 'html.parser')
    browser.quit()

    #get data
    tables = pd.read_html(facts_url)

    #save data
    mars_facts = tables[0]
    mars_facts.columns = ['Description', 'Mars','Earth']
    mars_facts = mars_facts.set_index('Description')

    #convert df to html table str
    facts_html = mars_facts.to_html()

    return facts_html


#Mars Hemisphere-Web Scraping
def scrape_hemispheres_images():  
   
    #set up
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
   
    #website
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)
   
    #htm to soup obj
    hemisphere_web = browser.html
    hemisphere_obj = BeautifulSoup(hemisphere_web, 'html.parser')
    browser.quit()
   
    #find image
    item_hemisphere_images = hemisphere_obj.find_all('div', class_="item")
   
    #loop & save
    mars_hemispheres_urls = []

    for item in item_hemisphere_images:
   
        try:
            mars_hemispheres_images = {}

            img_title_h3 = item.find_all('h3')
            img_title  = img_title_h3[0].text
            a  = item.find_all('a')
            a_url = a[0]['href']
           
            #save
            img_url = f"{hemisphere_url}{ a_url}"
            img_src = item.img['src']
            img_src_url = f"{hemisphere_url}{img_src}"
            mars_hemispheres_images['title']       =  img_title 
            mars_hemispheres_images['img_url']     =  img_url  
            mars_hemispheres_images['img_src_url'] =  img_src_url  
            mars_hemispheres_urls.append(mars_hemispheres_images)
           
        except AttributeError as e:
            print(e)
           
    return mars_hemispheres_urls

#Scrape
def scrape():  
    #NASA Mars News
    news_title, news_p = scrape_news()
   
    #JPL Mars Space Images
    featured_image_url = scrape_featured_image()
   
    #Mars Facts
    facts_html = scrape_facts()
   
    #Mars Hemisphere
    mars_hemispheres_urls = scrape_hemispheres_images()
   
    #save data to dict                              
    mars_scrape_data = { "news_title"         : news_title
                       , "news_p"             : news_p
                       , "featured_image_url" : featured_image_url
                       , "facts_html"         : facts_html 
                       , "hemispheres_images" : mars_hemispheres_urls 
                       }
   
    return  mars_scrape_data