from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # ### NASA Mars News

    url='https://redplanetscience.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')
   

    # News Title and Paragraph
    news_title=soup.find_all('div', class_='content_title')[0].text
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text

    print('-'*100)
    print(news_title)
    print(news_p)
    print('-'*100)


    # ### JPL Mars Space Images - Featured Image

    img_url='https://spaceimages-mars.com/'
    browser.visit(img_url)
    html=browser.html
    soup=bs(html,'html.parser')


    # Image url for the current Featured Mars Image
    image_path = soup.find_all('img', class_='headerimage fade-in')[0]['src']
    featured_image_url = img_url + image_path
    print(featured_image_url)


    # ### Mars Facts

    facts_url='https://galaxyfacts-mars.com/'
    browser.visit(facts_url)



    # Mars Facts
    Mars_Facts = pd.read_html(facts_url)[1]
    Mars_Facts.columns = ['Features','Data']
    Mars_Facts # I chose this table because it hahd more info about mars, hope it's ok

    # To html
    html_table = Mars_Facts.to_html()
    html_table.replace('\n','')
    print(html_table)


    # ### Mars Hemispheres


    hemis_url='https://marshemispheres.com/'
    browser.visit(hemis_url)
    html=browser.html
    soup=bs(html,'html.parser')


    # Getting article and items
    article=soup.find('div',class_='collapsible results')
    items=article.find_all('div',class_='item')

    hemisphere_image_urls=[]

    for item in items:
        
        # Title
        search=item.find('div',class_='description')
        title=search.h3.text
        
        # Image url
        hemis_href=search.a['href']
        browser.visit(hemis_url+hemis_href)
        html=browser.html
        soup=bs(html,'html.parser')        
        image_src=soup.find('li').a['href']
                
        # Creating dictionaries
        hem_dict={
            'title':title,
            'image_url':hemis_url + image_src
            }
        # Appending to list
        hemisphere_image_urls.append(hem_dict)
        
        print('-'*100)
        print(title)
        print(hemis_url + image_src)
    
    mars_dict = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "html_table":html_table,
        "hemisphere_images":hemisphere_image_urls
        }
    
    browser.quit()

    return mars_dict