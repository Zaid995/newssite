import json
import lxml
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from datetime import datetime, date
import traceback

class GetNews:

    def __init__(self):
        self.session = requests.Session()


    def parse_date(self, date_string):
        months = {
            'јануари': 'January',
            'февруари': 'February',
            'март': 'March',
            'април': 'April',
            'мај': 'May',
            'јуни': 'June',
            'јули': 'July',
            'август': 'August',
            'септември': 'September',
            'октомври': 'October',
            'ноември': 'November',
            'декември': 'December'
        }
        for mk_month, en_month in months.items():
            if mk_month in date_string:
                date_string = date_string.replace(mk_month, en_month)
                break
        try:
            date = datetime.strptime(date_string, '%B %d, %Y').date()
        except ValueError:
            try:
                date = datetime.strptime(date_string, '%B %d %Y').date()
            except ValueError:
                date = datetime.today().strftime('%Y-%m-%d')
        return date

    def kanal5(self):
        data = []
        response = self.session.get('https://kanal5.com.mk/sport')
        soup = BeautifulSoup(response.content, 'lxml')
        articles = soup.find_all('a', class_='article-title')
        pics = soup.find_all('div', class_='article-image')
        dates = soup.find_all('span', class_='article-date')

        for i, article in enumerate(articles):
            if i >= len(dates):
                break
            title = article.text.strip()
            link = 'https://kanal5.com.mk' + article['href']
            pic = 'https://kanal5.com.mk' + pics[i].find('img')['src']
            date = dates[i].text.strip()

            article_data = {
                'title': title,
                'link': link,
                'pic': pic,
                'date': date,
                'category': 'sport'
            }

            data.append(article_data)

        return data



    def republika(self):
        url = 'https://republika.mk/category/izbori2020/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        articles = soup.find_all('article')
        data = []
        for article in articles:
            title = article.find('h2').text.strip()
            link = article.find('a')['href']
            try:
                date = article.find('time').text.strip()
            except:
                date = ''
            data.append({'source': 'Republika', 'title': title, 'link': link, 'date': date})
        return data

    def VOA(self):
        url = 'https://mk.voanews.com/z/1733'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        articles = soup.select('div.media-block__content a')
        titles = soup.select('h4.media-block__title')
        pics = soup.find_all('div', class_='thumb thumb16_9')
        dates = soup.find_all('span', class_='date')
        data = []
        added_links = set()

        for i, article in enumerate(articles):
            href = article.get('href')
            if 'https://' not in href:
                href = 'https://mk.voanews.com/' + href
            pic = pics[i].find('img')['src']
            date_string = dates[i].text.strip()
            date = self.parse_date(date_string)
            if date is None:
                continue
            if href in added_links:
                continue
            added_links.add(href)
            article_data = {
                'title': titles[i].text.strip(),
                'link': href,
                'pic': pic,
                'date': date,
                'category': 'svet'
            }
            data.append(article_data)
        return data

    def irl(self):
        url = 'https://irl.mk/mk/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        articles = soup.select('h2.post-title a')
        pictures = soup.select('div.featured-image img')
        dates = soup.find_all('div', class_='post-byline')
        data = []

        for article, pic, date in zip(articles, pictures, dates):
            title = article.text.strip()
            link = article.get('href').strip()
            picture_url = pic.get('src')
            date_string = date.text.strip()
            date = datetime.strptime(date_string, '%d.%m.%Y').strftime('%Y-%m-%d')
            article_data = {
                'title': title,
                'link': link,
                'pic': picture_url,
                'date': date,
                'category': 'macedonia'
            }
            data.append(article_data)
        return data

    def mms(self):
        url = 'https://mms.mk/mkd/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        articles = soup.select('a.p-flink')
        dates = soup.find_all('time', class_='date published')

        data = []
        for article, date in zip(articles, dates):
            title = article.get('title').strip()
            link = article.get('href').strip()
            picture_url = article.select_one('img')['src']
            date_string = date.text
            date = datetime.strptime(date_string, '%d/%m/%Y').strftime('%Y-%m-%d')
            article_data = {
                'title': title,
                'link': link,
                'pic': picture_url,
                'date': date,
                'category': 'macedonia'
            }
            data.append(article_data)
        return data

    def denesen(self):
        url = 'https://denesen.mk'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        articles = soup.select('h2.article-title.l-black.lh-1.h5 a[title]')
        dates = soup.find_all('span', class_='date')
        data = []
        for i, article in enumerate(articles):
            title = article['title'].strip()
            link = article['href'].strip()
            response = self.session.get(link)
            soup = BeautifulSoup(response.text, 'lxml')
            picture = soup.select_one('div.featured-img img')
            picture_url = picture['src']
            date = dates[i].text
            article_data = {
                'title': title,
                'link': link,
                'pic': picture_url,
                'date': date,
                'category': 'opsto'
            }
            data.append(article_data)
        return data

    def biznis(self):
        url = 'https://www.biznisvesti.mk/category/ekonomija/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        articles = soup.select('h2.post-box-title')
        dates = soup.find_all('span', class_='tie-date')
        data = []

        for i, article in enumerate(articles):
            a_tag = article.find('a')
            link = a_tag['href'].strip()
            response = self.session.get(link)
            soup = BeautifulSoup(response.content, 'lxml')
            title = soup.select_one('h1.entry-title').text.strip()
            #pic = soup.find('div', class_='single-post-thumb')
            #picture_url = pic.find('img')['src']
            date_string = dates[i].text.strip()
            date = datetime.strptime(date_string, '%d/%m/%Y').strftime('%Y-%m-%d')
            article_data = {
                'title': title,
                'link': link,
                #'pic': picture_url,
                'date': date,
                'category': 'economy'
            }
            data.append(article_data)
        return data

    def alfa(self):
        url = 'https://alfa.mk/kategorija/vesti/skopje/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        articles = soup.find_all('figcaption')
        dates = soup.find_all('span', class_='item-metadata posts-date')
        pics = soup.find_all('div', class_='data-bg-hover data-bg-categorised read-bg-img')
        data = []
        for i, article in enumerate(articles):
            title = article.text.strip()
            link = article.find('a')['href'].strip()
            picture_url = pics[i].find('img')['src'].strip()
            date_string = dates[i].find('a').text.strip()
            date = datetime.strptime(date_string, '%d.%m.%Y').strftime('%Y-%m-%d')
            article_data = {
                'title': title,
                'link': link,
                'pic': picture_url,
                'date': date,
                'category': 'macedonia'
            }
            data.append(article_data)
        return data

    def faktor(self):
        url = 'https://faktor.mk/balkan'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        articles = soup.find_all('div', class_='article')
        data = []
        for article in articles:
            link = 'https://faktor.mk/' + article.find('a')['href'].strip()
            title = article.find('img')['alt'].strip()
            picture_url = 'https://faktor.mk' + article.find('img')['src']
            response = self.session.get(link)
            soup = BeautifulSoup(response.content, 'lxml')
            date_string = soup.find('span', class_='date').text.strip()
            date = self.parse_date(date_string)
            article_data = {
                'title': title,
                'link': link,
                'pic': picture_url,
                'date': date,
                'category': 'balkan'
            }
            data.append(article_data)
        return data

    def novamakedonija(self):
        url = 'https://novamakedonija.com.mk/category/zivot/kultura/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        articles = soup.find_all('div', class_="td-module-thumb")
        dates = soup.find_all('span', class_='td-post-date')
        x = 0

        data = []
        for i, article in enumerate(articles):
            title = article.find('a')['title'].strip()
            link = article.find('a')['href'].strip()
            picture_url = article.find('img')['src']
            if x >= len(dates):
                break
            date_string = dates[x].find('time').text
            datetime_obj = datetime.strptime(date_string, '%H:%M %d.%m.%Y')
            date = datetime_obj.date()
            article_data = {
                'title': title,
                'link': link,
                'pic': picture_url,
                'date': date,
                'category': 'culture'
            }
            data.append(article_data)
            x += 1
        return data

    def plusinfo(self):
        url = 'https://plusinfo.mk/category/bs-skopje/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('a', class_="img-holder")
        dates = soup.find_all('span', class_='time')
        data = []
        for i in range(len(articles)):
            article = articles[i]
            title = article.get('title').strip()
            link = article.get('href').strip()
            pic = article.get('style').replace('background-image: url(', '').replace(');', '')
            date_string = dates[i].find('time').text.strip()
            date = datetime.strptime(date_string, '%d/%m/%Y').strftime('%Y-%m-%d')
            article_data = {
                'title': title,
                'link': link,
                'pic': pic,
                'date': date,
                'category': 'skopje'
            }
            data.append(article_data)
        return data

    def vocentar(self):
        url = 'https://vocentar.com/category/bs-science/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_="featured clearfix")
        dates = soup.find_all('span', class_='time')
        data = []
        for i in range(len(articles)):
            if articles[i].find('a'):
                article = articles[i].find('a')
                title = article['title'].strip()
                link = article['href'].strip()
                pic = article['data-src']
                date_string = dates[i].find('time').text
                date = self.parse_date(date_string)

                article_data = {
                    'title': title,
                    'link': link,
                    'pic': pic,
                    'date': date,
                    'category': 'svet'
                }
                data.append(article_data)
        return data

    def dajgas(self):
        url = 'https://dodajgas.mk/category/svet/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_="archive-page-item-box")
        dates = soup.find_all('div', class_='blog-post-meta-date')
        links = soup.find_all('div', class_='blog-post-title-and-excerpt-wrap')
        data = []
        for article, date, link in zip(articles, dates, links):
            if article.find('a'):
                title = article.find('img')['alt'].strip()
                pic = article.find('img')['data-src']
                date_text = date.text.strip()
                try:
                    date = datetime.strptime(date_text, '%d/%m/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    date = ''
                if link.find('a'):
                    href = link.find('a')['href']
                article_data = {
                    'title': title,
                    'link': href,
                    'pic': pic,
                    'date': date,
                    'category': 'svet'
                }
                data.append(article_data)
        return data

    def IPON(self):
        url = 'https://ipon.mk/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_="td-module-thumb")
        dates = soup.find_all('div', class_='td-editor-date')
        data = []
        seen_links = set()
        for article, date in zip(articles, dates):
            title = article.find('a')['title']
            pic = article.find('span', class_='entry-thumb td-thumb-css')['data-img-url']
            link = article.find('a')['href'].strip()
            if link in seen_links:
                continue
            seen_links.add(link)
            date_text = date.text.strip()
            try:
                date = datetime.strptime(date_text, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                date = datetime.today().date()

            article_data = {
                'title': title,
                'link': link,
                'pic': pic,
                'date': date,
                'category': 'sport'
            }
            data.append(article_data)
        return data

    def Albania(self):
        url = 'https://www.balkanweb.com/kategoria/shqiperia/'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_="news-block-list-item")
        data = []
        for article in (articles):
            href = article.find('a')['href']
            title = article.find('h4').text.strip()
            pic = article.find('img')['src']
            date_text = article.find('p', class_='news-additional-info')
            date_string = date_text.find('span', class_='news-published-on').text
            try:
                date = GetNews().parse_date(date_string)

            except ValueError:
                date = 'N/A'
            article_data = {
                'title': title,
                'link': href,
                'pic': pic,
                'date': date,
                'category': 'Albania'
            }
            data.append(article_data)
        return data

    def to_json(self, data):
        def date_encoder(obj):
            if isinstance(obj,date):
                return obj.isoformat()
            raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")

        return json.dumps(data, default=date_encoder)


    def scrape_all(self):
        print('started')
        all_data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_results = [executor.submit(getattr(self, name)) for name in dir(self)
                              if callable(getattr(self, name)) and not name.startswith("__")
                              and name != "scrape_all" and name != 'parse_date' and name != 'to_json']
            for future in concurrent.futures.as_completed(future_results):
                try:
                    result = future.result()
                    if result:
                        all_data.extend(result)
                except Exception as e:
                    function_name = [name for name in dir(self)
                                     if callable(getattr(self, name)) and not name.startswith("__")
                                     and name != "scrape_all" and name != 'parse_date' and name != 'to_json'
                                     and getattr(self, name) == future][0]
                    print(f"An exception occurred in {function_name}:")
                    traceback.print_exc()

        json_data = self.to_json(all_data)

        with open('static/news_data.json', 'w', encoding='utf-8') as f:
            f.write(json_data)

        print('process finished')






