import json
from steam_worker import Steam_price
import market
import dbworker

class Compressor:
	"""docstring for Compressor"""
	def __init__(self,game=None,popularity=None,min_price=None,max_price=None):
		config = self.config_read()
		self.game = config['game']
		self.popularity = int(config['popularity'])
		self.min_price = int(config['min_price'])
		self.max_price = int(config['max_price'])

	@staticmethod
	def config_read():
		config_file = json.load(open('config.json'))
		return {'game':config_file['game'],'popularity':config_file['popularity'],'min_price':config_file['min_price'],"max_price":config_file['max_price']}
		
	def calculate_one(item):
		if type(item) == dict:
			to_steam = (item['steam_price']/1.15-item['tm_price'])/item['tm_price']*100
			to_market = (item['tm_price']/1.05-item['steam_price'])/item['steam_price']*100
			return {'name':item['name'],'to_steam_df':round(to_steam,2),'to_tm_df':round(to_market,2)}
		else:
			return item

	def calculate_all():
		items = dbworker.databases().get_items()
		for item in items:
			try:
				to_steam = round((item['steam_price']/1.15-item['tm_price'])/item['tm_price']*100,2)
				to_market = round((item['tm_price']/1.05-item['steam_price'])/item['steam_price']*100,2)
				print(item)
				print({'name':item['name'],'to_steam_df':to_steam,'to_tm_df':to_market})
				dbworker.databases().difference_writer({'name':item['name'],'to_steam_df':to_steam,'to_tm_df':to_market})
			except:
				print(item)