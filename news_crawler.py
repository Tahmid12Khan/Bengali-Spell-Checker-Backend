from bs4 import BeautifulSoup
import re
import requests
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

def crawl_prothom_alo(start_date_str, end_date_str):
    from datetime import datetime, timedelta
    base_url = "https://www.prothomalo.com"
    archive_url = base_url+"/archive/"
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    delta = end_date - start_date
    for i in range(delta.days + 1):

        date = start_date + timedelta(days = i)
        url = archive_url+date.strftime("%Y-%m-%d")
        infile = open('Newspaper/prothom_alo_'+ date.strftime("%Y-%m-%d") + ".txt", "w+", encoding = 'utf-8')
        while url:
            print("reading url >>> "+url)
            try:
                html_content = requests.get(url, headers = headers).content
            except:
                print('Connection Problem for url: ', url, '. Skipping it.')
                break
            soup = BeautifulSoup(html_content, "lxml")
            links = soup.findAll('a', {'class': 'link_overlay'}, href = True)
            for link in links:
                try:
                    inner_html_content = requests.get(base_url+link['href'], headers = headers).content
                except:
                    print('Connection Problem for article, url: ', base_url+link['href'])
                    continue
                inner_soup = BeautifulSoup(inner_html_content, "lxml")
                articleBody = inner_soup.find('div', {'itemprop': 'articleBody'})
                if articleBody:
                    headline = inner_soup.find('div', {'class': 'right_title'}).text
                    print("headline >>> "+headline)
                    infile.write(headline+"\n")
                    infile.write(str(articleBody.text) + '\n\n')
			
            pagination_div = soup.find('div', {'class': 'pagination'})
            url = None
            if pagination_div:
                next_page_link = pagination_div.find('a', {'class': 'next_page'}, href = True)
                if next_page_link:
                    url = next_page_link['href']
        infile.close()
		

	# crawl_prothom_alo("2017-03-08","2017-06-01")
crawl_prothom_alo("2019-08-03","2019-09-01")

