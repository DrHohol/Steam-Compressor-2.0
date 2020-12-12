import sqlite3
import steam_worker

class databases():
	"""docstring for databases"""
	def __init__(self, idbase=None,itemsbase=None):
		self.idbase = sqlite3.connect('databases/id_base.db')
		self.itemsbase = sqlite3.connect('databases/items.db')
		self.itemsbase_cursor = self.itemsbase.cursor()
		self.idbase_cursor = self.idbase.cursor()

	def write_tm(self,items):
		for item in items:
			self.itemsbase_cursor.execute("SELECT Name FROM items WHERE Name=?",(item['name'],))
			if self.itemsbase_cursor.fetchone():
				self.itemsbase_cursor.execute("UPDATE items SET TM_Price=?,TM_Autobuy=?,Avg=?,Popularity=? WHERE Name=?",(item['tm_price'],item['tm_buy'],item['avg'],item['popularity'],item['name']))
			else:
				print(self.itemsbase_cursor.fetchall())
				self.itemsbase_cursor.execute("INSERT INTO items(TM_Price,TM_Autobuy,Avg,Name,Popularity) VALUES(?,?,?,?,?)",(item['tm_price'],item['tm_buy'],item['avg'],item['name'],item['popularity']))
		self.itemsbase.commit()
		print("Обновлена база тм")

	def get_nameid(self,name):
		try:
			nameid = self.idbase_cursor.execute("SELECT id FROM items WHERE name=?",(name,))
			nameid = nameid.fetchall()[0]
			return nameid[0]
		except IndexError:
			nameid = steam_worker.Steam_price.get_id(name)
			self.add_id(name,nameid)
			return nameid

	def add_id(self,name,nameid):
		self.idbase_cursor.execute("INSERT INTO items(name,id) VALUES(?,?)",(name,nameid))
		self.idbase.commit()

	def write_steam(self,itemdata):
		try:
			self.itemsbase_cursor.execute("UPDATE items SET Steam_price=?,Autobuy_steam=? WHERE Name=?",(float(itemdata['steam_price']),float(itemdata['steam_buy']),itemdata['name']))
			self.itemsbase.commit()
		except:
			print(itemdata)

	def difference_writer(self,item):
		if type(item) == dict:
			self.itemsbase_cursor.execute("UPDATE items SET Difference_to_steam=?,Difference_to_tm=? WHERE Name=?",(item['to_steam_df'],item['to_tm_df'],item['name']))
			self.itemsbase.commit()
		else: pass

	def get_items(self):
		self.itemsbase_cursor.execute('SELECT Name,Steam_price,TM_Price From items')
		items = self.itemsbase_cursor.fetchall()
		items_list = []
		for item in items:
			if item[1] != '' and item[1] != None:
				items_list.append({'name':item[0],'steam_price':item[1],'tm_price':item[2]})
		return items_list