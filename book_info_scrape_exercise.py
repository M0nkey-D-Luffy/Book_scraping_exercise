from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError


def get_soup(url):
    try:
        html=urlopen(url)
    except HTTPError as he:
        print('Error : '+str(he))
        html=None
    if html==None:
        print('None obj will be returned')
        return html
    return BeautifulSoup(html)

def scrape_page(domain,soup):
    '''
    Get domain name and soup obj of current page
    and print Name,Price and ISBN of all books of page
    '''
    body=soup.findAll('div',class_='content')[1] 
    navi_bar=body.findChild()
    book_list=navi_bar.findNextSiblings()[:-1]
    global book_num
    for book in book_list:
        book_info=book.findChild().attrs
        book_link=book.find('a',href=True)['href']
        isbn=get_book_ISBN(domain,book_link)
        try:
            print(book_num)
            book_num+=1
            print('Book name  : '+book_info['data-product-title'])
            print('Book price : '+book_info['data-product-price'])
            print('Book ISBN  : '+isbn)
            print('***************'*2)
        except KeyError as ke:
            continue

def get_book_ISBN(domain,book_link):
    url=domain+book_link
    soup=get_soup(url)
    isbn=soup.find('div',class_='book-info-isbn13').find('span',itemprop='isbn').get_text()
    return isbn    


def get_next_page(soup):
    '''
    Return the url suffix of 'Next' page
    '''
    working_page='/all-books?search=&offset={}&rows=24&sort='
    get_next=lambda tag: tag.get_text()=='Next' 
    offset_value=soup.find(get_next)['data-offset']
    return working_page.format(offset_value)


domain='https://www.packtpub.com'
starting_page='/all-books?search=&offset={}&rows=24&sort='
book_num=1
current_working_soup=get_soup(domain+starting_page)
while current_working_soup is not None:
    scrape_page(domain,current_working_soup)
    next_page=get_next_page(current_working_soup)
    current_working_soup=get_soup(domain+next_page)


        
    
    
