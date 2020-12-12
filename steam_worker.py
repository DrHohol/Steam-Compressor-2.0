from dbworker import databases
import requests
import re

class Steam_price:
	"""docstring for Steam_price"""
	def __init__(self,steam_link=None):
		self.steam_link = "https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid="
		self.get_db = databases()

	def get_prices(self,item):
		nameid = self.get_db.get_nameid(item['name'])
		if nameid != None:
			try:
				item_data = requests.get(self.steam_link+nameid, proxies={"http":"http://WkI2rzLUvL:QwTZ5IYG12@91.188.231.172:60676"}).json()

				return {'name':item['name'],'steam_price':float(item_data['lowest_sell_order'])/100,'steam_buy':float(item_data['highest_buy_order'])/100,
				'tm_price':item['tm_price']}
			except: return "Ошибка стим"
		else:
			return "Нет на торговой площадке"

	def get_id(item):
		print(item)
		try:
			item_page = requests.get("https://steamcommunity.com/market/listings/570/"+item).content
			result = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(item_page))
			nameid = str(result[0])
		except IndexError:
			try:
				item_page = requests.get("https://steamcommunity.com/market/listings/730/"+item).content
				result = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(item_page))
				nameid = str(result[0])
			except:
				nameid = None
		return nameid