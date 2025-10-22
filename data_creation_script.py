import random
import mysql.connector
from faker import Faker


DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASSWORD = ''  
DB_NAME = 'Assignment_2'



def generate_author(fake: Faker, author_id: int) -> tuple:
    name = fake.name()
    country = fake.country()
    return (author_id, name, country)


def generate_reader(fake: Faker, reader_id: int) -> tuple:
    name = fake.name()
    city = fake.city()
    membership = random.choice(['Active', 'Inactive', 'Premium', 'VIP'])
    return (reader_id, name, city, membership)


def generate_book(fake: Faker, book_id: int, max_author_id: int) -> tuple:
    title = fake.catch_phrase()
    author_id = random.randint(1, max_author_id)
    year = random.randint(1950, 2024)
    price = round(random.uniform(5.99, 49.99), 2)
    return (book_id, title, author_id, year, price)




def insert_authors(total_rows: int = 1_000_000, batch_size: int = 10_000) -> None:
    
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    fake = Faker()
    
    insert_query = "INSERT INTO authors (id, name, country) VALUES (%s, %s, %s)"
    
    print(f"authors")
    
    author_id = 1
    for i in range(0, total_rows, batch_size):
        batch = []
        for _ in range(min(batch_size, total_rows - i)):
            record = generate_author(fake, author_id)
            batch.append(record)
            author_id += 1
        
        cursor.executemany(insert_query, batch)
        connection.commit()
        print(f"  → {i + len(batch):,} / {total_rows:,} rows")
    
    cursor.close()
    connection.close()
    print("✅ Authors\n")


def insert_readers(total_rows: int = 1_500_000, batch_size: int = 10_000) -> None:
    
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    fake = Faker()
    
    insert_query = "INSERT INTO readers (id, name, city, membership_status) VALUES (%s, %s, %s, %s)"
    
    print(f"Readers")
    
    reader_id = 1
    for i in range(0, total_rows, batch_size):
        batch = []
        for _ in range(min(batch_size, total_rows - i)):
            record = generate_reader(fake, reader_id)
            batch.append(record)
            reader_id += 1
        
        cursor.executemany(insert_query, batch)
        connection.commit()
        print(f"  → {i + len(batch):,} / {total_rows:,} rows")
    
    cursor.close()
    connection.close()
    print("✅ Readers\n")




def insert_books(total_authors: int, total_rows: int = 2_000_000, batch_size: int = 10_000) -> None:
    
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    fake = Faker()
    
    insert_query = "INSERT INTO books (id, title, author_id, year_published, price) VALUES (%s, %s, %s, %s, %s)"
    
    print(f"Books ")
    
    book_id = 1
    for i in range(0, total_rows, batch_size):
        batch = []
        for _ in range(min(batch_size, total_rows - i)):
            record = generate_book(fake, book_id, total_authors)
            batch.append(record)
            book_id += 1
        
        cursor.executemany(insert_query, batch)
        connection.commit()
        print(f"  → {i + len(batch):,} / {total_rows:,} rows")
    
    cursor.close()
    connection.close()
    print("✅ Books \n")



if __name__ == "__main__":

    AUTHORS_COUNT = 1_000_000
    READERS_COUNT = 1_000_000
    BOOKS_COUNT = 1_000_000
    
    insert_authors(total_rows=AUTHORS_COUNT, batch_size=10_000)
    insert_readers(total_rows=READERS_COUNT, batch_size=10_000)
    insert_books(total_authors=AUTHORS_COUNT, total_rows=BOOKS_COUNT, batch_size=10_000)
    
