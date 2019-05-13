from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import re

def init_browser():
   # @NOTE: Replace the path with your actual path to the chromedriver
   executable_path = {"executable_path": "chromedriver.exe"}
   return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    endpoint_dict = {}


#first Mars story on page
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

#title and teaser from Mars story

    title = soup.find("div", class_="content_title")
    teaser = soup.find("div", class_="article_teaser_body")
    endpoint_dict["news_title"]= title.text
    endpoint_dict["news"]=teaser.text
 
#mars images
    urlimage = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    start_url = 'https://www.jpl.nasa.gov'
    browser.visit(urlimage)

    time.sleep(1)

    htmlimage = browser.html
    soupimage = bs(htmlimage, "html.parser")
    picture= soupimage.find("article", class_= "carousel_item")
    part1= picture['style'].split('\'')
    featured_image = (start_url + part1[1])
    endpoint_dict['featured_image'] = featured_image


#latest weather on mars

    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)

    time.sleep(1)

    htmltwitter = browser.html
    souptwitter = bs(htmltwitter, "html.parser")
    picture2 =souptwitter.find("p", class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    endpoint_dict["weather_data"] = picture2.text

#mars table data
    url_table = "https://space-facts.com/mars/"
    table = pd.read_html(url_table)
    table[0].columns=["Description", "Value"]
    table[0].set_index("Description", inplace=True)
    mars_table = table[0].to_html()
    endpoint_dict["mars_table"] = mars_table

#hemisphere pics and titles
    urlhemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    part_url = 'https://astrogeology.usgs.gov'
    browser.visit(urlhemi)


    time.sleep(1)

    htmlhemi = browser.html
    souphemi = bs(htmlhemi, "html.parser")
    hemi = souphemi.find_all("div", class_= "description")
    h_data = {}
    h_final_data = []


#links for hemisphere pics
    for h in hemi:
        hpic = h.find("a")
        pic_title = h.find("h3")
        get_pic = (part_url + hpic["href"])
        h_data[pic_title.text] = get_pic

#urls for hemi pics
    for v in h_data.keys():
        browser.visit(h_data[v])

        time.sleep(1)

        tmp_html = browser.html
        tmp_soup = bs(tmp_html, "html.parser")
        tmp_data = tmp_soup.find_all("div", class_= "downloads")

        for final in tmp_data:
            link_f = final.find("li")
            h_final_data.append({"title":v, "link":link_f.a["href"]})

    
    endpoint_dict["hemispheres"]= h_final_data

    return endpoint_dict


