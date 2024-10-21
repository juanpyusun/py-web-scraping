# Librerias
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime as dt
import random

# VariablURLes
URL1 = "https://scrapepark.org/courses/spanish/"
URL2 = "http://en.wikipedia.org/wiki/Kevin_Bacon"
URL3 = "http://en.wikipedia.org"
URL4 = "https://www.oreilly.com/"
URL5 = "http://www.pythonscraping.com/pages/page3.html"


WIKI_ARTICLE = "/wiki/Kevin_Bacon"
allExtLinks = []
allIntLinks = []
pages = set()

# Funciones
def url_to_soup(url):
  html = requests.get(url)
  soup = BeautifulSoup(html.content, 'html.parser')
  return soup

def images(url):  
  soup = url_to_soup(url)
  src_todos = soup.find_all(src=True)
  
  url_imagenes = []
  for i, imagen in enumerate(src_todos):
    if imagen['src'].endswith('png'):

      print(imagen['src'])
      r = requests.get(url+f"{imagen['src']}")

      with open(f'imagen_{i}.png', 'wb') as f:
        f.write(r.content)
   
def response_headers():  
  url = "http://httpbin.org/headers"
  headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
  # Peticiones con y sin headers
  request = requests.get(url)
  print(f"Respuesta sin headers:\n{request.text}")

  request = requests.get(url, headers = headers)
  print(f"Respuesta con headers: \n {request.text}")
  
def api():
  latitud = -34.6
  longitud = -58.4
  fecha = "1816-07-09" # AAAA-MM-DD
  request = requests.get(f"https://api.sunrise-sunset.org/json?lat={latitud}&lng={longitud}&date={fecha}")
  print(f"Respuesta de la api sunrise-sunset:\n{request.json()['results']['sunset']}")

def find_by_element(url):
  soup = url_to_soup(url)  
  print(soup.find("h1"))
  print(soup.find("h1").text)
  print(soup.h1.text)
  
def find_by_element_3(url):
  soup = url_to_soup(url)  
  titles = soup.find_all(['h1', 'h2','h3','h4','h5','h6'])
  print(titles)

def find_by_class(url):
  soup = url_to_soup(url)  
  divs = soup.find_all('div', class_ = "heading-container heading-center")
  print(divs)

def find_by_tag(url):
  soup = url_to_soup(url)  
  src_todos = soup.find_all(src=True)
  for elemento in src_todos:
    if elemento['src'].endswith(".jpg"):
      print(elemento)
    
def find_by_id(url):
  soup = url_to_soup(url)  
  divs = soup.find_all('div', id = "heading-container")
  print(divs)    

def get_tittle(url):
  soup = url_to_soup(url)
  print(soup.title.text)
  
def find_by_element_2(url):
  soup = url_to_soup(url)  
  nameList = soup.findAll('div', {'class': ['hero-area', 'attribution']})
  for name in nameList:
      print(name.attrs)

def find_links(url):  
  soup = url_to_soup(url)  
  links = soup.find_all('a')
  for link in soup.find('div', {'id':'bodyContent'}).find_all(
      'a', href=re.compile('^(/wiki/)((?!:).)*$')):
      print(link.attrs['href'])

def find_articles(url):
  soup = url_to_soup(url)  
  for link in soup.find('div', {'id':'bodyContent'}).find_all(
    'a', href=re.compile('^(/wiki/)((?!:).)*$')):
    print(link.attrs['href'])
  
def getLinks(url, articleUrl):
    html = requests.get(url+articleUrl)
    soup = BeautifulSoup(html.content, 'html.parser')
    return soup.find('div', {'id':'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))
  
def random_walk(url, articleUrl):
  random.seed(dt.now().microsecond)
  links = getLinks(url, articleUrl)
  while len(links) > 0:
      newArticle = links[random.randint(0, len(links)-1)].attrs['href']
      print(newArticle)
      links = getLinks(url,newArticle)

def getLinks2(pageUrl):
  # Recursively crawling an entire site
    soup = url_to_soup(URL3+pageUrl)
    for link in soup.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks2(newPage)
                
def getLinks3(pageUrl):
  # Collecting Data Across an Entire Site
    soup = url_to_soup(URL3+pageUrl)
    try:
        print(soup.h1.get_text())
        #mw-parser-output
        bodyContent = soup.find('div', {'id':'bodyContent'}).find_all('p')
        if len(bodyContent):
            print(bodyContent[0])
        print(soup.find(id='ca-edit').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something! Continuing.')
    
    for link in soup.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print('-'*20)
                print(newPage)
                pages.add(newPage)
                getLinks3(newPage)

# Retrieves a list of all internal links found on a page
def getInternalLinks(bs, base_url):
    internalLinks = set()
    for link in bs.find_all('a', href=True):
        href = link['href']
        # Resolve relative URLs and check if the link is internal
        full_url = requests.compat.urljoin(base_url, href)
        if full_url.startswith(base_url):
            internalLinks.add(full_url)
    return list(internalLinks)

# Retrieves a list of all external links found on a page
def getExternalLinks(bs, base_url):
    externalLinks = set()
    for link in bs.find_all('a', href=True):
        href = link['href']
        # Resolve relative URLs and check if the link is external
        full_url = requests.compat.urljoin(base_url, href)
        if not full_url.startswith(base_url):
            externalLinks.add(full_url)
    return list(externalLinks)

def getRandomExternalLink(startingPage):
    response = requests.get(startingPage)
    bs = BeautifulSoup(response.text, 'html.parser')
    externalLinks = getExternalLinks(bs, startingPage)
    if not externalLinks:
        print('No external links, looking around the site for one')
        internalLinks = getInternalLinks(bs, startingPage)
        if not internalLinks:
            return None
        return getRandomExternalLink(random.choice(internalLinks))
    else:
        return random.choice(externalLinks)

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    if externalLink:
        print(f'Random external link is: {externalLink}')
        followExternalOnly(externalLink)
    else:
        print('No more external links found.')
        
def getAllExternalLinks(url):
    bs = BeautifulSoup(urlopen(url), 'html.parser')
    internalLinks = getInternalLinks(bs, url)
    externalLinks = getExternalLinks(bs, url)
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.append(link)
            print(link)

    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.append(link)
            getAllExternalLinks(link)
        
def get_childs(url):
  soup = url_to_soup(url)  
  for child in soup.find('table',{'id':'giftList'}).children:
    print(child)        

def get_siblings(url):
  soup = url_to_soup(url)  
  for sibling in soup.find('table', {'id':'giftList'}).tr.next_siblings:
    print(sibling)  
    
def get_parent_previous_sibling(url):      
  soup = url_to_soup(url)  
  print(soup.find('img',
                {'src':'../img/gifts/img1.jpg'})
        .parent.previous_sibling.get_text())

def get_using_regex(url):      
  soup = url_to_soup(url)
  images = soup.find_all('img', {'src':re.compile('\.\.\/img\/gifts/img.*\.jpg')})
  for image in images: 
      print(image['src'])  
      
def get_using_lambda(url):      
  soup = url_to_soup(url)
  tags = soup.find_all(lambda tag: len(tag.attrs) == 2)
  for tag in tags:
    print(tag)
        
def get_using_lambda_2(url):      
  soup = url_to_soup(url)
  tags = soup.find_all(lambda tag: tag.get_text() == 'Or maybe he\'s only resting?')
  for tag in tags:
    print(tag)
    
def get_using_lambda_3(url):      
  soup = url_to_soup(url)
  tags = soup.find_all('', text='Or maybe he\'s only resting?')
  for tag in tags:
    print(tag)
    
if __name__ == "__main__":  
  #response_headers()
  #api()
  #get_tittle(URL1)
  #find_by_element(URL1)
  #find_by_class(URL1)
  #find_by_id(URL1)
  #find_by_tag(URL1)
  #images(URL1)
  #find_by_element_2(URL1)
  #find_by_element_3(URL1)
  #find_links(URL2)
  #find_articles(URL2)
  #random_walk(URL3, WIKI_ARTICLE)
  #getLinks2('')
  #getLinks3('/wiki/General-purpose_programming_language')
  #followExternalOnly(URL4)
  #allIntLinks.append(URL4.replace('www.', ''))
  #getAllExternalLinks(URL4)
  #get_childs(URL5)
  #get_siblings(URL5)
  #get_parent_previous_sibling(URL5)
  #get_using_regex(URL5)
  #get_using_lambda(URL5)
  #get_using_lambda_2(URL5)
  #get_using_lambda_3(URL5)
  pass
  
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# crawlers
# algunos ejemplos
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Primero
from bs4 import BeautifulSoup
from urllib.request import urlopen

class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body
    
    def print(self):
        print(f'TITLE: {self.title}')
        print(f'URL: {self.url}')
        print(f'BODY:\n {self.body}')

def scrapeCNN(url):
    bs = BeautifulSoup(urlopen(url))
    title = bs.find('h1').text
    body = bs.find('div', {'class': 'article__content'}).text
    print('body: ')
    print(body)
    return Content(url, title, body)

def scrapeBrookings(url):
    bs = BeautifulSoup(urlopen(url))
    title = bs.find('h1').text
    body = bs.find('div', {'class': 'post-body'}).text
    return Content(url, title, body)

url = 'https://www.brookings.edu/research/robotic-rulemaking/'
content = scrapeBrookings(url)
content.print()

url = 'https://www.cnn.com/2023/04/03/investing/dogecoin-elon-musk-twitter/index.html'
content = scrapeCNN(url)
content.print()


# Segundo
class Content:
    """
    Common base class for all articles/pages
    """
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """
        Flexible printing function controls output
        """
        print(f'URL: {self.url}')
        print(f'TITLE: {self.title}')
        print(f'BODY:\n{self.body}')

class Website:
    """ 
    Contains information about website structure
    """
    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        
# Tercero
from bs4 import BeautifulSoup


class Crawler:
    def getPage(url):
        try:
            html = urlopen(url)
        except Exception:
            return None
        return BeautifulSoup(html, 'html.parser')

    def safeGet(bs, selector):
        """
        Utilty function used to get a content string from a Beautiful Soup
        object and a selector. Returns an empty string if no object
        is found for the given selector
        """
        selectedElems = bs.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def getContent(website, path):
        """
        Extract content from a given page URL
        """
        url = website.url+path
        bs = Crawler.getPage(url)
        if bs is not None:
            title = Crawler.safeGet(bs, website.titleTag)
            body = Crawler.safeGet(bs, website.bodyTag)
            return Content(url, title, body)
        return Content(url, '', '')
        
# Cuarto
siteData = [
    ['O\'Reilly Media', 'https://www.oreilly.com', 'h1', 'div.title-description'],
    ['Reuters', 'https://www.reuters.com', 'h1', 'div.ArticleBodyWrapper'],
    ['Brookings', 'https://www.brookings.edu', 'h1', 'div.post-body'],
    ['CNN', 'https://www.cnn.com', 'h1', 'div.article__content']
]
websites = []
for name, url, title, body in siteData:
    websites.append(Website(name, url, title, body))

Crawler.getContent(websites[0], '/library/view/web-scraping-with/9781491910283').print()
Crawler.getContent(
    websites[1], '/article/us-usa-epa-pruitt-idUSKBN19W2D0').print()
Crawler.getContent(
    websites[2],
    '/blog/techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/').print()
Crawler.getContent(
    websites[3], 
    '/2023/04/03/investing/dogecoin-elon-musk-twitter/index.html').print()
    
# Quinto
class Content:
    """Common base class for all articles/pages"""

    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):
        """
        Flexible printing function controls output
        """
        print(f'New article found for topic: {self.topic}')
        print(f'URL: {self.url}')
        print(f'TITLE: {self.title}')
        print(f'BODY:\n{self.body}')
        
# Sexto
class Website:
    """Contains information about website structure"""

    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        
# Septimo
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, website):
        self.site = website
        self.found = {}

    def getPage(url):
        try:
            html = urlopen(url)
        except Exception as e:
            return None
        return BeautifulSoup(html, 'html.parser')

    def safeGet(bs, selector):
        """
        Utilty function used to get a content string from a Beautiful Soup
        object and a selector. Returns an empty string if no object
        is found for the given selector
        """
        selectedElems = bs.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def getContent(self, topic, url):
        """
        Extract content from a given page URL
        """
        bs = Crawler.getPage(url)
        if bs is not None:
            title = Crawler.safeGet(bs, self.site.titleTag)
            body = Crawler.safeGet(bs, self.site.bodyTag)
            return Content(topic, url, title, body)
        return Content(topic, url, '', '')

    def search(self, topic):
        """
        Searches a given website for a given topic and records all pages found
        """
        bs = Crawler.getPage(self.site.searchUrl + topic)
        searchResults = bs.select(self.site.resultListing)
        for result in searchResults:
            url = result.select(self.site.resultUrl)[0].attrs['href']
            # Check to see whether it's a relative or an absolute URL
            url = url if self.site.absoluteUrl else self.site.url + url
            if url not in self.found:
                self.found[url] = self.getContent(topic, url)
            self.found[url].print()



siteData = [
    ['Reuters', 'http://reuters.com', 'https://www.reuters.com/search/news?blob=', 'div.search-result-indiv',
        'h3.search-result-title a', False, 'h1', 'div.ArticleBodyWrapper'],
    ['Brookings', 'http://www.brookings.edu', 'https://www.brookings.edu/search/?s=',
        'div.article-info', 'h4.title a', True, 'h1', 'div.core-block']
]
sites = []
for name, url, search, rListing, rUrl, absUrl, tt, bt in siteData:
    sites.append(Website(name, url, search, rListing, rUrl, absUrl, tt, bt))

crawlers = [Crawler(site) for site in sites]
topics = ['python', 'data%20science']

for topic in topics:
    for crawler in crawlers:
        crawler.search(topic)

# Octavo
class Website:

    def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Content:

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f'URL: {self.url}')
        print(f'TITLE: {self.title}')
        print(f'BODY:\n{self.body}')
        
# Noveno
import re


class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = {}

    def getPage(url):
        try:
            html = urlopen(url)
        except Exception as e:
            print(e)
            return None
        return BeautifulSoup(html, 'html.parser')

    def safeGet(bs, selector):
        selectedElems = bs.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def getContent(self, url):
        """
        Extract content from a given page URL
        """
        bs = Crawler.getPage(url)
        if bs is not None:
            title = Crawler.safeGet(bs, self.site.titleTag)
            body = Crawler.safeGet(bs, self.site.bodyTag)
            return Content(url, title, body)
        return Content(url, '', '')

    def crawl(self):
        """
        Get pages from website home page
        """
        bs = Crawler.getPage(self.site.url)
        targetPages = bs.findAll('a', href=re.compile(self.site.targetPattern))
        for targetPage in targetPages:
            url = targetPage.attrs['href']
            url = url if self.site.absoluteUrl else f'{self.site.url}{targetPage}'
            if url not in self.visited:
                self.visited[url] = self.getContent(url)
                self.visited[url].print()


brookings = Website('Reuters', 'https://brookings.edu', '\/(research|blog)\/', True, 'h1', 'div.post-body')
crawler = Crawler(brookings)
crawler.crawl()

# Decimo
class Website:
    """Common base class for all articles/pages"""

    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        
# Decimo pimero
class Product(Website):
    """Contains information for scraping a product page"""

    def __init__(self, name, url, titleTag, productNumber, price):
        Website.__init__(self, name, url, TitleTag)
        self.productNumberTag = productNumberTag
        self.priceTag = priceTag

class Article(Website):
    """Contains information for scraping an article page"""

    def __init__(self, name, url, titleTag, bodyTag, dateTag):
        Website.__init__(self, name, url, titleTag)
        self.bodyTag = bodyTag
        self.dateTag = dateTag
        
