from urllib.parse import parse_qs, urlsplit, urljoin
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = 'https://www.google.com'
SEARCH_URL = BASE_URL + '/search'

def get_param_from_url(url, param):
     querystring = urlsplit(url).query
     value_list = parse_qs(querystring).get(param)
     if value_list is None:
         return None
     else:
         return value_list[0]

def is_full_url(url):
    url_tuple = urlsplit(url)
    if url_tuple.netloc:
        return True
    else:
        return False

class ResultPage(object):

    def __init__(self, q, start=0):
        self.q = q
        self.start = start
        self.soup = self.get_soup()
        self.results = [Result(g_tag) for g_tag in self.soup.find_all('div', class_='g')]

    def __repr__(self):
        return '<\'{}\' ({})>'.format(self.q, self.start)

    def get_soup(self):
        payload = {'q' : self.q, 'start' : self.start}
        response = requests.get(SEARCH_URL, params=payload)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def get_next_page(self):
        nav_table = self.soup.find('table', id='nav')
        if not nav_table:
            raise StopIteration
        next_a_tag = nav_table.find('td', class_='b', style='text-align:left').a
        if not next_a_tag:
            raise StopIteration
        href = next_a_tag.attrs.get('href')
        start = int(get_param_from_url(href, 'start'))
        return self.__class__(q=self.q, start=start)

    def get_previous_page(self):
        nav_table = self.soup.find('table', id='nav')
        if not nav_table:
            raise StopIteration
        prev_a_tag = nav_table.find('td', class_='b', style=False).a
        if not prev_a_tag:
            raise StopIteration
        href = prev_a_tag.attrs.get('href')
        start = int(get_param_from_url(href, 'start'))
        return self.__class__(q=self.q, start=start)

class Result(object):

    def __init__(self, g_tag):
        self.g_tag = g_tag
        self.title = self.get_title()
        self.url = self.get_url()
        self.description = self.get_description()

    def __repr__(self):
        return '<Result: {} ({})>'.format(self.title, self.url)

    @staticmethod
    def is_title_tag(tag):
        if tag.name == 'a' and not tag.find('img'):
            return True
        else:
            return False

    def get_title(self):
        title = self.g_tag.find(self.is_title_tag).get_text()
        # a_tag = self.g_tag.a
        # if a_tag is None:
        #     return ''
        # title = a_tag.get_text()
        return title

    def get_url(self):
        href = self.g_tag.find(self.is_title_tag).attrs.get('href')
        if is_full_url(href):
            return href
        elif re.match(r'/search', href):
            return urljoin(BASE_URL, href)
        else:
            return get_param_from_url(href, 'q')

    def get_description(self):
        description_tag = self.g_tag.find('span', class_='st')
        if description_tag is None:
            return None
        description = description_tag.get_text()
        description = re.sub(r'\n', '', description)
        return description

class Search(object):

    def __init__(self, q):
        self.q = q
        self.pages = [ResultPage(self.q, 0)]

    def __repr__(self):
        return '<Search: {}>'.format(self.q)

    def fetch_next_page(self):
        """Fetch next page to cache. Raises StopIteration if last page is reached"""
        self.pages.append(self.pages[-1].get_next_page())

    def page_generator(self):
        """yields result list from each page"""
        for p in self.pages:
            yield p.results
        while True:
            self.fetch_next_page()
            yield self.pages[-1].results

    def results(self, stop=10):
        out = []
        page_iterator = self.page_generator()
        while len(out) < stop:
            try:
                page = next(page_iterator)
            except StopIteration:
                return out
            out.extend(page)
        return out[:stop]
