import bs4
from bs4 import BeautifulSoup
import requests

url = "http://www.4wd.com/Jeep-Tires-Jeep-Tire-Accessories/Tires.aspx?t_c=13&t_s=536&t_pt=101509"

r = requests.get(url)
data=r.text

soup = BeautifulSoup(data)

##prodcut pricing parent class
nameStr= soup.find_all("ul", {"class" : "productOverview"})

#priceList= []
for name in nameStr:
	print name.find("li").find("h3").find('a',href=True).get_text().lstrip().rstrip()

#for link in soup.find_all('a', href = True ):
#	print(link['href'])
