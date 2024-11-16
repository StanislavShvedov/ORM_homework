import json
from pprint import pprint

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_table, Publisher, Book, Shop, Stock, Sale
from config import USER_NAME, PASSWORD, DATA_NAME
import os

DSN = f'postgresql://{USER_NAME}:{PASSWORD}@localhost:5432/{DATA_NAME}'
engine = sqlalchemy.create_engine(DSN)

if __name__ == '__main__':
    create_table(engine)

    with open('fixtures/tests_data.json', 'r') as f:
        data = json.load(f)

    Session = sessionmaker(bind=engine)
    session = Session()

    publishers = []
    books = []
    shops = []
    stocks = []
    sales = []
    for i in range(len(data)):
        if data[i]['model'] == 'publisher':
            publisher = Publisher(name=data[i]['fields']['name'])
            session.add(publisher)
            publishers.append(publisher)

        elif data[i]['model'] == 'book':
            book = Book(title=data[i]['fields']['title'], id_publisher=data[i]['fields']['id_publisher'])
            session.add(book)
            books.append(book)

        elif data[i]['model'] == 'shop':
            shop = Shop(name=data[i]['fields']['name'])
            session.add(shop)
            shops.append(shop)

        elif data[i]['model'] == 'stock':
            stock = Stock(id_shop=data[i]['fields']['id_shop'], id_book=data[i]['fields']['id_book'],
                         count=data[i]['fields']['count'])
            session.add(stock)
            stocks.append(stock)

        elif data[i]['model'] == 'sale':
            sale = Sale(price=data[i]['fields']['price'], date_sale=data[i]['fields']['date_sale'],
                         count=data[i]['fields']['count'], id_stock=data[i]['fields']['id_stock'])
            session.add(sale)
            sales.append(sale)

    session.commit()

    print('Авторы:')
    for i in publishers:
        print(f'---{i}')
    print('Книги:')
    for i in books:
        print(f'---{i}')
    print('Магазины:')
    for i in shops:
        print(f'---{i}')
    for i in stocks:
        print(f'---{i}')
    for i in sales:
        print(f'---{i}')

    session.close()
