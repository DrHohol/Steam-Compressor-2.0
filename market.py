import json
import requests
from Compressor import Compressor
from time import sleep
from dbworker import databases

class Market(Compressor):
	"""docstring for Market"""
	def __init__(self, cs_link=None,dota_link=None):
		Compressor.__init__(self)
		databases.__init__(self)
		self.cs_link = "https://market.csgo.com/api/v2/prices/class_instance/RUB.json"
		self.dota_link = "https://market.dota2.net/api/v2/prices/class_instance/RUB.json"

	def Parse(self):
		writer = databases()
		#while True:
		for_table = []
		if self.game == 'dota':
			items = requests.get(self.dota_link).json()['items']
		elif self.game  == 'csgo':
			items = requests.get(self.cs_link).json()['items']
		elif self.game == 'both':
			items = requests.get(self.dota_link).json()['items']
			csgo_items = (requests.get(self.cs_link).json()['items'])
			for i in csgo_items:
				items[i] = csgo_items[i]

		for skin in self.dupdel(items):
			if skin['popularity_7d'] != None and skin['avg_price'] != None:
				if int(skin['popularity_7d']) > self.popularity and float(skin['price']) >self.min_price and float(skin['price']) < self.max_price:
					for_table.append({
						'name':skin['market_hash_name'],'tm_price':float(skin['price']),'avg':round(float(skin['avg_price']),2),'tm_buy':skin['buy_order'],
						'popularity':skin['popularity_7d']
						})
		return for_table
		#	sleep(30)

	def dupdel(self,items):
		new = []
		tmp = []
		for i in items:
			if items[i]['market_hash_name'] not in tmp:
				new.append(items[i])
			else:
				tmp.append(items[i]['market_hash_name'])
		return new


