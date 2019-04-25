import bs4
from bs4 import BeautifulSoup
import requests

url = "http://www.4wd.com/Jeep-Tires-Jeep-Tire-Accessories/Tires.aspx?t_c=13&t_s=536&t_pt=101509"

r = requests.get(url)
data=r.text

soup = BeautifulSoup(data)

#prodcut pricing parent class
ppp= soup.find_all("ul", {"class" : "productPricing"})
#product pricing child class
ppc= soup.find_all("ul", {"class" : "price"})

priceList= []
for price in ppp:
	print price.find("strong", {"class": "price"}).get_text()

#for link in soup.find_all('a', href = True ):
#	print(link['href'])
