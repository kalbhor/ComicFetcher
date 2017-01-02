import requests
from bs4 import BeautifulSoup
import datetime
import re
import six
import argparse

if six.PY2:
    from urllib2 import urlretrieve
    from urllib2 import quote
    input = raw_input
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlretrieve

FILE_TYPE = '.png'
now = datetime.datetime.now() 
DATE = str(now.day)+'-'+str(now.month)+'-'+str(now.year)

def main():
	parser = argparse.ArgumentParser(description="Download various comics")
	parser.add_argument('--cyanide', action='store_true', help='Download latest cyanide and happiness comic')
	parser.add_argument('--xkcd', action='store_true', help='Download latest xkcd comic')
	parser.add_argument('--channelate', action='store_true', help='Download latest channelate comic')

	args = parser.parse_args()

	if args.cyanide:
		explosm()

	if args.xkcd:
		xkcd()

	if args.channelate:
		channelate()


def explosm():
	find = re.compile( r'.+?(?=' + re.escape(FILE_TYPE) + r')' )
	response = requests.get('http://explosm.net/')
	soup = BeautifulSoup(response.text, 'html.parser')
	comic_src = soup.find('img', {'id' : 'featured-comic'}).get('src')

	found = re.match(find,comic_src).group()	
	comic_url = 'http:'+found+FILE_TYPE
	file_name ='Cyanide {} {}'.format(DATE, found.split('/')[-1])
	urlretrieve(comic_url, file_name + FILE_TYPE)
	print('Saved %s'%(file_name))

def xkcd():
	response = requests.get('http://xkcd.com/info.0.json').json()
	comic_url = response['img']
	file_name = 'xkcd {} {}'.format(DATE, response['title'])
	print(comic_url)
	urlretrieve(comic_url, file_name + FILE_TYPE)
	print('Saved %s'%file_name)

def channelate():

	response = requests.get('http://www.channelate.com/')
	print(response.status_code)
	soup = BeautifulSoup(response, 'html.parser')
	comic_tag = soup.find('div', {'class':'comicpane'}).find('img')
	comic_url = "{https}{url}".format(https='http:', url=comic_tag.get('src'))
	file_name = "Channelate {} {comic_name}".format(DATE,comic_name=comic_tag.get('title'))
	print(comic_url)
	urlretrieve(comic_url, "lol.png")
	print('Saved %s'%(file_name))



if __name__ == '__main__':
	main()