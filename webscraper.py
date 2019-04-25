import requests
import bs4
import csv
import unicodecsv
import itertools

amazonSearch = "http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
wikipedia = "https://en.wikipedia.org/wiki/"
# 4WD isn't considered a string, so python wants to interpret it as a number
FWDTires = "http://www.4wd.com/Jeep-Tires-Jeep-Tire-Accessories/Tires.aspx?t_c=13&t_s=536&t_pt=101509"


def getlist(URL, item):
    # this gets all links from a wikipedia search
    # response is the raw html for a web page, this includes the references to the json objects in a file
    response = requests.get(URL+item)
    # if you just print response, it will give you a reference to it rather than the text itself
    # print response.text
    # soup is an object to look at parsed items
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # in this soup I'm trying to find all items that are within <> </> that are links, so <a href="some/url/extension">the link name</a>
    links = soup.find_all('a', href=True)
    # printing it will give me two the things the <a> and the text within </a>
    print links
    for link in links:
        # for the links, use the dictionary, for the words used, use .get_text()
        print link['href']


def getUL(subclass):
    items = []
    for overView in subclass:
        ul = overView.find("ul", {"class": "specs"}).find_all("li")
        liList = []
        for li in ul:
            liList.append(li.get_text())
        items.append(liList)
    return items


def crawlPages(URL, maxPage):
    finishedproduct = []

    firstResponse = requests.get(URL)
    soup = bs4.BeautifulSoup(firstResponse.text, 'html.parser')
    prices = soup.find_all("ul", {"class": "productPricing"})
    overViewList = soup.find_all("ul", {"class": "productOverview"})
    items = getUL(overViewList)

    headings = []
    for overView in overViewList:
        headings.append(overView.find("li").find("h3").find(
            'a', href=True).get_text().lstrip().rstrip())

    priceParsed = []
    #find_all("ul", {"class": "specs"})
    for price in prices:
        # print price.find(class_="price").get_text()
        priceParsed.append(price.find(class_="price").get_text())
    print finishedproduct
    finishedproduct = zip(headings, priceParsed, items)
    print finishedproduct
    # going to iterate through the list, so in 4WD, the first page is unique and the subsequent pages have a '&p=' appended to the end

    # items=[]
    for page in range(2, maxPage):
        restResponse = requests.get(URL+'&pg='+str(page))
        soup = bs4.BeautifulSoup(restResponse.text, 'html.parser')
        prices = soup.find_all("ul", {"class": "productPricing"})
        overViewList = soup.find_all("ul", {"class": "productOverview"})

        #####################################
        # get all the extranaeous information of the object, like tire size, sidewall etc
        items = getUL(overViewList)
        #####################################

        #####################################
        # single for loop, look for the prices within the larger 'price' object
        priceParsed = []
        for price in prices:
            priceParsed.append(price.find(class_="price").get_text())
        #####################################

        ####################################
        headings = []
        for overView in overViewList:
            headings.append(overView.find("li").find("h3").find(
                'a', href=True).get_text().lstrip().rstrip())
        ####################################

        finishedproduct = finishedproduct+zip(headings, priceParsed, items)
    return finishedproduct


def savetocsv(data):
    with open("tireInfo.csv", "w") as outfile:
        writer = unicodecsv.writer(
            outfile, quoting=csv.QUOTE_ALL, encoding='utf-8')
        # writer.writerow(colnames)
        for line in range(len(data)):
            row = []
            row.append(data[line][0])
            row.append(data[line][1])

            for item in data[line][2]:
                row.append(item)

            writer.writerow(row)
        print "Done Processing to file"


def main():
    # getlist(wikipedia, "wrenches")
    # going through the first 10 pages of tires listing, returning the lowest cost tires, didn't see a sort function
    hugeArray = crawlPages(FWDTires, 10)
    savetocsv(hugeArray)


if __name__ == "__main__":
    main()
