import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json

class Play:

	def __init__(self):

		self.URL = 'https://www.playscripts.com'
		self.NPGS = 0
		self.plays = []

	def setup(self):
		"""
		look at the starting page to find out how many pages to scrape
		"""
		try:
			soup = BeautifulSoup(requests.get(self.URL + '/find-a-play?').text, 'lxml')
		except:
			print(f'can\'t create a soup object, have to stop right here...')
			return self

		# find the first pagination thing
		try:
			self.NPGS = int(soup.find('div', class_='pagination').find('li', class_='last-page').find('a').text.strip())
			print(f'pages to scrape: {self.NPGS}')
		except:
			print(f'can\'t figure out the total number of pages, sorry..')
			return self

		return self

	def collect(self, file):

		# grab each page
		for i in range(self.NPGS):

			if (i + 1)%10 == 0:
				print(f'page {i + 1}/{self.NPGS}...')

			try:
				soup = BeautifulSoup(requests.get(self.URL + '/find-a-play?page=' + str(i)).text, 'lxml')
			except:
				print(f'can\'t create a soup object for page {i}...')
				return self

			for p in soup.find_all('div', class_='theater-story'):

				_play_info = defaultdict(str)

				_play_info['name'] = p.find('h3').find('a').text.lower().strip()
				_play_info['author'] = p.find('h3').find('span').find('a').text.lower().strip()
				_play_info['genre'] = p.find('div', class_='movie-info').find('li').text.lower().strip()

				self.plays.append(_play_info)

		json.dump(self.plays, open(file, 'w'))
		print(f'done. saved data ({len(self.plays)} plays)  in {file}')

		return self

if __name__ == '__main__':

	p = Play().setup().collect(file='plays.json')