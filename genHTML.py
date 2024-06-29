from bs4 import BeautifulSoup
import requests

class Generate:
    def __init__(self, folderPath, filePath):
        '''
        Initializes the html file and further organizes information from csv into a list
        '''
        self.filePath = filePath
        csv = open(filePath, 'r')
        self.html = open(f'{folderPath}\index.html','w')
        self.html.write(f'<!DOCTYPE html>\n<head>\n<title>PokeChart</title>\n<link rel="stylesheet" type="text/css" href="../app.css">\n</head>\n<html>\n<title>HTML Tutorial</title>\n<body>\n')
        self.cards = []
        for row in csv:
            try:
                row = row.strip().split(',')
                row = {
                    'card':row[0],
                    'ungraded':row[1],
                    'PSA-10':row[2],
                    'quantity':row[3],
                    'link':row[4]
                }
                self.cards.append(row)
            except:
                return

    def generate(img,attributes):
        '''
        Generates the HTML relevant to each card
        
        param: 
            attributes: a dict() containing card attributes
        '''
        s = ''
        if 'pricecharting' in attributes['link']:
            s += f'<div class="card">\n<h1>{attributes['card']}</h1>\n<br>\n<div class="image">\n<img src="{img['src']}" alt="{img['alt']}">\n</div>\n<h2>Ungraded: {attributes['ungraded']}</h2>\n<h3>PSA-10: {attributes['PSA-10']}</h3>\n</div>\n'
        elif 'trollandtoad' in attributes['link']:
            s += f'<div class="noCard">\n<h1>{attributes['card']}</h1>\n<br>\n<p>No image available</p>\n<h2>Ungraded: {attributes['ungraded']}</h2>\n<h3>PSA-10: {attributes['PSA-10']}</h3>\n</div>\n'
        return s

    def retrieveImg(page):
        '''
        Visits webpage html and scrapes image url. Does not work for troll and toad currently
        
        params: 
            page: Page() object from PokeGen.py
        '''
        if 'pricecharting' in page.url:
            img = page.page.find('div', attrs={'class':'cover'})
            imgSrc = img.find('img')['src']
            imgAlt = img.find('img')['alt']
            attributes = {
                'src':imgSrc,
                'alt':imgAlt
            }
            return attributes
        elif 'trollandtoad' in page.url:
            attributes = {
                'src':'N/A',
                'alt':'N/A'
            }
            return attributes