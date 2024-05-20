from bs4 import BeautifulSoup
import requests
from datetime import date
import os
from genHTML import Generate

DATE = date.today()

class File:

    def __init__(self, file = "pokemon.csv"):
        self.file = open(file, 'r')
        self.links, self.names, self.quantity = [], [], []
        for i in self.file:
            i = i.strip().split(',')
            self.names.append(i[0])
            self.links.append(i[1])
            self.quantity.append(i[2])

    def __str__(self):
        s = ''
        for i in range(len(self.names)):
            s += f'{self.names[i]}: {self.links[i]} [{self.quantity[i]}]\n'
        return s

class Page:

    def __init__(self, url):
        self.url = url
        self.page = requests.get(url)
        self.page = BeautifulSoup(self.page.text, 'html.parser')
        self.attributes = self.organize(self.page)

    def organize(self, page):
        attributes = {
                    'card': None,
                    'price': None,
                    'PSA-10': None
                    }
        if 'pricecharting' in self.url:
            card = page.find('h1', attrs={'class':'chart_title'}).text.strip()
            attributes['card'] = card

            price = page.find('span', attrs={'class':'price js-price'}).text.strip()
            attributes['price'] = price

            psa10 = page.find('span', attrs={'title': 'current Manual Only value','class':'price js-price'}).text.strip()
            attributes['PSA-10'] = psa10
        elif 'trollandtoad' in self.url:
            card = page.find('h1', attrs={'class':'font-weight-bold font-large font-md-largest mt-1 product-name'}).text.strip()
            attributes['card'] = card

            price = page.find('span', attrs={'id':'sale-price', 'class':'d-none'}).text.strip()
            attributes['price'] = price

            attributes['PSA-10'] = 'N/A'
        else:
            attributes['card'] = 'N/A'
            attributes['price'] = 'N/A'
            attributes['PSA-10'] = 'N/A'

        return attributes

def __main__():
    file = File()
    today = DATE
    date = str(today.strftime('%m.%d.%y'))
    newPath = f'PokeChart_{date}'
    filePath = f'PokeChart_{date}\PokeLog.csv'
    if not os.path.exists(newPath):
        os.makedirs(newPath)
    newFile = open(filePath, 'w')
    newFile.write('card,ungraded,PSA 10,quantity,links\n')
    sum = 0
    psaSum = 0
    for i in range(len(file.links)):
        page = Page(file.links[i])
        s = f'{file.names[i]},{page.attributes['price']},{page.attributes['PSA-10']},{file.quantity[i]},{file.links[i]}\n'
        if '$' in page.attributes['price']:
            sum += float(page.attributes['price'][1:])*float(file.quantity[i])
        else:
            sum += float(page.attributes['price'])*float(file.quantity[i])
        if '$' in page.attributes['PSA-10']:
            psaSum += float(page.attributes['PSA-10'][1:])*float(file.quantity[i])
        newFile.write(s)
        print(f'{file.names[i]}\nMarket: {page.attributes['price']}\nPSA-10: {page.attributes['PSA-10']}\n')
    sum = round(sum, 2)
    newFile.write(f'\n,Collection Sum, PSA 10 Sum,,\n,${sum},${psaSum},,')
    newFile.close()
    newFile = open(filePath, 'r')
    
    pokeHtml = Generate(newPath, filePath)
    
    for i in range(len(file.links)):
        img = Generate.retrieveImg(Page(file.links[i]))
        pokeHtml.html.write(Generate.generate(img,pokeHtml.cards[i+1]))
    pokeHtml.html.write(f'<h1>Total Sum: ${sum}</h1>\n<h2>PSA-10 Sum: ${psaSum}</h2>\n</body>')
        
        

if __name__ == '__main__':
    __main__()