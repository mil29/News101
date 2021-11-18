from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as bs
import requests
import re
import random


def home(request):
    
    # Get array of input buttons value to see which news buttons requested
    if request.method == 'POST':
        if len(request.POST.getlist('news_select')) > 0:
            request.session['user_data'] = request.POST.getlist('news_select')
            return redirect('news_feed')
    
    return render(request, 'articles/home.html', {})



def news_feed(request):
    
    # Get request input button values from home view
    url_data = request.session.get('user_data')
    # print(url_data)
    
    # Arrays of news urls to check against 
    urllist = [
        'https://www.bbc.co.uk/news',
        'https://www.theguardian.com/uk',
        'https://metro.co.uk/news/uk/',
        'https://news.sky.com/uk',
        'https://techcrunch.com',
        'https://www.reuters.com/world/uk/',
    ]
    
    # Array to hold all news data
    titles = []
    hrefs = []
    newspaper = []
    logo = []
    
    # Loop through selected inputs to scrape web content
    for url in urllist:
        for val in url_data:
            if val == url:
                url = url
                article = requests.get(url)
                soup = bs(article.content, 'html.parser')
                
                
                # Scrape news media channels finding title of article, href link to news site
                
                # BBC
                if url == "https://www.bbc.co.uk/news":
                    body = soup.find("div", {"id": 'nw-c-topstories-domestic'})
                    # titles
                    h3s = []
                    for h3 in body.find_all('h3', 'gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text'):
                        h3s.append(h3.text)

                    
                    # Removing duplicates from articles h3s array
                    removed_duplicates = list(dict.fromkeys(h3s))
                    for h3 in removed_duplicates:
                        titles.append(h3)
                    
                    # href links 
                    href_link = body.find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')
                    first_href_check = []
                    for a in href_link:
                        first_href_check.append(a['href'])
                        
                    # Removing duplicates from href links from first_href_link array
                    removed__href_duplicates = list(dict.fromkeys(first_href_check))
                    for a in removed__href_duplicates:
                        hrefs.append('https://www.bbc.co.uk' + a)
                        # newspaper name
                        newspaper.append("BBC")
                        logo.append('BBC_News.png')
                        

                # The Guardian
                if url == "https://www.theguardian.com/uk":
                    body = soup.find("section", {"id": "headlines"})
                    # titles
                    for h3 in body.find_all('h3'):
                        titles.append(h3.text)
                    # href links    
                    href_link = body.find_all('a', class_='fc-item__link')
                    for a in href_link:
                        hrefs.append(a['href'])
                        # newspaper name
                        newspaper.append('The Guardian')
                        logo.append('theguardian.jpg')
                        
                # Metro
                if url == "https://metro.co.uk/news/uk/":
                    body = soup.find("div", {"id": "mosaic-channel-zone-wrapper"})
                    # titles
                    for h3 in body.find_all('h3', class_='metro__post__title'):
                        titles.append(h3.text)
                    # href links  
                    href = body.find_all('a')
                    for a in href[0:21:3]:
                        hrefs.append(a['href'])
                        # newspaper name
                        newspaper.append('Metro')
                        logo.append('metro.jpg')
                        
                        
                # Sky News
                if url == "https://news.sky.com/uk":
                    body = soup.find("div", {"class": "sdc-site-tiles__inner"})
                    # titles
                    for h3 in body.find_all('h3', class_='sdc-site-tile__headline'):
                        titles.append(h3.text)
                    # href links  
                    href_link = body.find_all('a', class_='sdc-site-tile__headline-link')
                    for a in href_link:
                        hrefs.append('https://news.sky.com/story' + a['href'])
                        # newspaper name
                        newspaper.append('Sky News')
                        logo.append('Sky-news.png')
                        
                        
                # Techcrunch
                if url == "https://techcrunch.com":
                    body = soup.find("div", {"class": "river river--homepage"})
                    # titles
                    for h2 in body.find_all('h2', class_='post-block__title'):
                        titles.append(h2.text)
                    # href links  
                    href_link = body.find_all('a', class_='post-block__title__link')
                    for a in href_link:
                        hrefs.append(a['href'])
                        # newspaper name
                        newspaper.append('Techcrunch')
                        logo.append('techcrunch.png')
                        
                        
                # Reuters
                if url == "https://www.reuters.com/world/uk/":
                    body = soup.find("div", {"class": "LandingLayout__main___2_3Sj_"})
                    # titles
                    for span in body.find_all('span', class_='Text__text___3eVx1j Text__dark-grey___AS2I_p Text__medium___1ocDap Text__heading_6___m3CqfX Heading__base___1dDlXY Heading__heading_6___1ON736 MediaStoryCard__heading___1K4tAO'):
                        titles.append(span.text)
                    # href links  
                    href_link = body.find_all('a', class_='MediaStoryCard__hub___2ECKOi story-card')
                    for a in href_link:
                        hrefs.append('https://www.reuters.com' + (a['href']))
                        # newspaper name
                        newspaper.append('Reuters')
                        logo.append('Reuters-Logo.jpg')
                    
                    
                
    
    # Zip all 3 arrays with news data for context in template
    news = zip(titles, hrefs, newspaper, logo)
    
    # Randomizing articles along with links
    r_news = list(zip(titles, hrefs, newspaper, logo))
    random.shuffle(r_news)
    zip(*r_news)
    
    context = {
    "newspaper": newspaper,
    'titles': titles,
    'hrefs': hrefs,
    'news': news,
    'r_news': r_news,
    'logo': logo
    }     
    # print(len(titles))
    # print(len(hrefs))
    # print(r_news)
    
                  
    return render(request,'articles/news_feed.html', context)
                
     