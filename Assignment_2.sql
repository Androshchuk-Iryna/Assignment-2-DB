DROP DATABASE IF EXISTS Assignment_2;
CREATE DATABASE Assignment_2;
USE Assignment_2;

CREATE TABLE authors (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE readers (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    membership_status VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE books (
    id INT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_id INT,
    year_published INT,
    price DECIMAL(6,2)
) ENGINE=InnoDB;

SHOW TABLES;
DESCRIBE authors;
DESCRIBE readers;
DESCRIBE books;

SELECT COUNT(*) FROM authors;
SELECT COUNT(*) FROM readers;
SELECT COUNT(*) FROM books;


