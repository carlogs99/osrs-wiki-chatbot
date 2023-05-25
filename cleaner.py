import wikitextparser as wtp
from bs4 import BeautifulSoup
import os

def read_article(article, filename):
  wiki_parse = wtp.parse(str(article))
  art_sec_titles = [s.title for s in wiki_parse.sections]
  if art_sec_titles.count('Changes') > 0:
    del wiki_parse.sections[art_sec_titles.index('Changes')].string
  if art_sec_titles.count('Gallery') > 0:
    del wiki_parse.sections[art_sec_titles.index('Gallery')].string
  with open(filename, 'w') as file:
    file.write(str(wiki_parse))

def read_wiki_xml(filename):
  with open(filename, 'r') as f:
    data = f.read()
  Bs_data = BeautifulSoup(data, "xml")
  articles = Bs_data.find_all('text')
  titles = Bs_data.find_all('title')
  os.mkdir('articles')
  for i in range(len(articles)):
    read_article(articles[i], f'./articles/{titles[i].contents[0].replace(" ","_")}.txt')

read_wiki_xml("wiki.xml")