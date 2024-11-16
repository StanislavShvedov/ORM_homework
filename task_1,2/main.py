from typing import Any
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_table, Publisher, Book, Shop, Stock, Sale
from config import USER_NAME, PASSWORD, DATA_NAME

DSN = f'postgresql://{USER_NAME}:{PASSWORD}@localhost:5432/{DATA_NAME}'
engine = sqlalchemy.create_engine(DSN)

if __name__ == '__main__':
    create_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    publisher1 = Publisher(name='Пушкин')
    publisher2 = Publisher(name='Гоголь')
    session.add_all([publisher1, publisher2])
    session.commit()

    book_1 = Book(title='Капитанская дочка', id_publisher=publisher1.id)
    book_2 = Book(title='Руслан и Людмила', id_publisher=publisher1.id)
    book_3 = Book(title='Евгений Онегин', id_publisher=publisher1.id)
    book_4 = Book(title='Вий', id_publisher=publisher2.id)
    session.add_all([book_1, book_2, book_3, book_4])
    session.commit()

    shop_1 = Shop(name='Буквоед')
    shop_2 = Shop(name='Лабиринт')
    shop_3 = Shop(name='Книжный дом')
    session.add_all([shop_1, shop_2, shop_3])
    session.commit()

    stock_1 = Stock(count=2, id_book=1, id_shop=1)
    stock_2 = Stock(count=1, id_book=2, id_shop=1)
    stock_3 = Stock(count=1, id_book=1, id_shop=2)
    stock_4 = Stock(count=1, id_book=3, id_shop=3)
    stock_5 = Stock(count=1, id_book=4, id_shop=3)
    session.add_all([stock_1, stock_2, stock_3, stock_4, stock_5])
    session.commit()

    sale_1 = Sale(price=600, date_sale='2022-11-09', count=1, id_stock=1)
    sale_2 = Sale(price=500, date_sale='2022-11-08', count=1, id_stock=2)
    sale_3 = Sale(price=580, date_sale='2022-11-05', count=1, id_stock=3)
    sale_4 = Sale(price=490, date_sale='2022-11-02', count=1, id_stock=4)
    sale_5 = Sale(price=600, date_sale='2022-10-26', count=1, id_stock=1)
    sale_6 = Sale(price=666, date_sale='2023-10-26', count=1, id_stock=5)
    session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5, sale_6])
    session.commit()


    def search_book(info: Any) -> None:
        """
        Функция для поиска по фамили или id информации о продажах книги
        :param info: принмает фамилию (string) или id (integer)
        """
        if info.isalpha():
            serach = (session.query(Publisher, Book, Stock, Shop, Sale)
                      .join(Book, Publisher.id == Book.id_publisher)
                      .join(Stock, Book.id == Stock.id_book)
                      .join(Shop, Shop.id == Stock.id_shop)
                      .join(Sale, Stock.id == Sale.id_stock)
                      .filter(Publisher.name == info)
                      .all())

            for c in serach:
                print(f'{c[1].title} | {c[3].name} | {c[4].price} | {c[4].date_sale}')

        if info.isdigit():
            serach = (session.query(Publisher, Book, Stock, Shop, Sale)
                      .join(Book, Publisher.id == Book.id_publisher)
                      .join(Stock, Book.id == Stock.id_book)
                      .join(Shop, Shop.id == Stock.id_shop)
                      .join(Sale, Stock.id == Sale.id_stock)
                      .filter(Publisher.id == info)
                      .all())

            for c in serach:
                print(f'{c[1].title} | {c[3].name} | {c[4].price} | {c[4].date_sale}')


    info = input('Введите фамилию автора или его id для поиска: ')
    search_book(info)

    session.close()
