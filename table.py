from steam_worker import Steam_price
from market import Market
from time import sleep
from dbworker import databases
from Compressor import Compressor
import threading

m = Market()
st = Steam_price()
def tm_checker():
	global itms
	m = Market()
	while True:
		itms = m.Parse()
		databases().write_tm(itms)
		Compressor.calculate_all()
		sleep(30)
threading.Thread(target=tm_checker,daemon=True).start()

while True:
	for i in m.Parse():
		print(i)
		price = st.get_prices(i)
		databases().write_steam(price)
		difference = Compressor.calculate_one(price)
		databases().difference_writer(difference)
		sleep(3)

