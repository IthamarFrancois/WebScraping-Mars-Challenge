# Dependencies
import pandas as pd
#import requests
import time
import datetime as dt
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def MarsTable():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)    
    ## Mars Facts
    ## URL of page to scrape
    url = 'https://galaxyfacts-mars.com/'
    time.sleep(1)

    GalaxyTable_DF = pd.read_html(url)
    MarsFactsTable = GalaxyTable_DF[1]
    MarsFactsTable.rename(columns = {0:'MARS DESCRIPTION', 1:'VALUE'}, inplace=True)
    
    ## Quit Browser client and return Mars Fact DF html table for index.html display
    browser.quit()
    return  MarsFactsTable.to_html(classes="table table-striped").replace('\n',"")


## Main scrape function
def scrape():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    ## Dictionary to hold all scraped data
    ScrapeData = {}
    
    ## ================  Scrape Instructions (Copied from Notebook) =============== ##
    
    ## NASA Mars News
    ## URL of page to scrape
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    
    
    ## HTML setup
    NewsHTML = browser.html
    NewsSoup = BeautifulSoup(NewsHTML, 'html.parser')
    
    ## Scrape article headline title and paragraph text/blerb
    NewsTitle = NewsSoup.find('div', class_ = 'col-md-12').find(class_='content_title').text
    NewsParagraph = NewsSoup.find('div', class_ = 'col-md-12').find(class_='article_teaser_body').text

    NewsParagraph = str(NewsParagraph)
    NewsTitle = str(NewsTitle)
    #print(f"News Title: {NewsTitle}")
    #print(f"Paragraph Blerb: '{NewsParagraph}'")
    browser.quit()


    ## --------------------------------------------------------------- ##
    

    ## JPL Mars Space Images
    ## Setup splinter, executable path, and Chrome web driver browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## URL of page to scrape
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    time.sleep(1)

    ## HTML setup
    JPLMarsHTML = browser.html
    JPLMarsSoup = BeautifulSoup(JPLMarsHTML, 'html.parser')
    
    ## Scrape website image path
    JPLMarsImageHTML = JPLMarsSoup.find('div', class_ = 'header').find(class_='floating_text_area')
    JPLMarsImageSRC = JPLMarsImageHTML.find('a')['href']

    ## Create image url by combining base URL with returned image path
    featured_image_url = f"{url}{JPLMarsImageSRC}" 
    #print(featured_image_url)
    browser.quit()


    ## --------------------------------------------------------------- ##
    
    ## Seperated Mars Fact table from scrap function to call seperately (leaving code for reference)
    ## Mars Facts
    ## URL of page to scrape
    #url = 'https://galaxyfacts-mars.com/'
    #time.sleep(1)

    #GalaxyTable_DF = pd.read_html(url)
    #GalaxyTable = GalaxyTable_DF[1]
    #GalaxyTable.head()

    #GalaxyTable.rename(columns = {0:'MARS DESCRIPTION', 1:'VALUE'}, inplace=True)
    ##GalaxyTable = GalaxyTable.set_index('MARS DESCRIPTION')
    ##GalaxyTable

    ## Converting dataframe back into HTML and removing line breaks ('\n')
    #GalaxyTable.to_dict(orient='records')
    #htmlTable = GalaxyTable.to_html(classes="table table-striped").replace('\n',"")
        
    ## Close webscrape session
    #browser.quit()
    
    
    ## --------------------------------------------------------------- ##
    
    ## Mars Hemispheres
    ## Setup splinter, executable path, and Chrome web driver browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## URL of page to scrape
    #Hemisphere_url = 'https://marshemispheres.com/'
    MarsHemis_url = 'https://marshemispheres.com/'
    browser.visit(MarsHemis_url)
    time.sleep(1)

    ## HTML setup
    MarsHemisHTML = browser.html
    MarsHemisSoup = BeautifulSoup(MarsHemisHTML, 'html.parser')

    ## Returns the HTML code containing ALL page links/div class
    MarsHemisphereHTML = MarsHemisSoup.find_all('div', {'class' : 'item'})

    ## For Loop and Dictionary Setup
    links = MarsHemisphereHTML
    Hemisphere_Image_URLS = []

    for link in range(len(links)):

        ## Code that select a SPECIFIC Hemisphere page based on index (Cerberus, Schiaparelli, Syrtis, Valles)
        NextMarsHemis = MarsHemisphereHTML[link]


        ## Scrape for the Hemisphere/image titles on homepage to add to dictionary
        MarsHemisImageTitle = NextMarsHemis.find('h3').text
        title = MarsHemisImageTitle
        #print(title)


        ## WebScraper command to go down the html page list by clicking the specific/current index "h3" link
        browser.find_by_tag("h3")[link].click()
        
        ## HTML Beautiful soup re-initialization for new hemisphere page
        MarsHemisHTML = browser.html
        MarsHemisSoup = BeautifulSoup(MarsHemisHTML, 'html.parser')


        ## Find Hemisphere partial image path
        HemisphereImageSRC = MarsHemisSoup.find('img', class_ = 'wide-image')['src']
        #HemisphereImageSRC


        ## Create full image url by combining base URL with returned image path
        FullHemisphereImageURL = f"{MarsHemis_url}{HemisphereImageSRC}" 
        img_url = FullHemisphereImageURL
        #print(img_url)

        ## Return back to homepage for next loop step
        browser.back()

        ## HTML Beautiful soup re-initialization for homepage to setup next loop
        MarsHemisHTML = browser.html
        MarsHemisSoup = BeautifulSoup(MarsHemisHTML, 'html.parser')


        ### Append scraped Title/Image Url data to dictionary
        Hemisphere_Image_URLS.append({ "Title": title, "IMG_URL": img_url })
        ## End of page scrape, next loop iteration
        


## --------------------------------------------------------------- ##
    ## Mars Fact function set to variable "Mars_Fact" to be appended into dictionary for Mongo DB    
    Mars_Fact = MarsTable()
    ScrapeData = {
        "News_Title" : NewsTitle,
        "News_Paragraph" : NewsParagraph,
        "Featured_Image" : featured_image_url,
        "Mars_Hemispheres" : Hemisphere_Image_URLS,
        "Mars_Facts" : Mars_Fact
        #"Mars_Table_HMTL" : htmlTable
    }
    
    ## Close webscrape session
    browser.quit()
    return ScrapeData


if __name__ == "__main__":
    print(scrape())

## ________________________________________ Ithamar Francois ______________________________________________________ ##
