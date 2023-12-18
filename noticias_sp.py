import requests
from bs4 import BeautifulSoup

response = requests.get('https://ge.globo.com/futebol/times/sao-paulo/')

content = response.content

site = BeautifulSoup(content, 'html.parser')

noticias = site.findAll('div', attrs={'class' : 'feed-post-body'})

for noticia in noticias:
    print(noticia.prettify())
    print('\n---\n')