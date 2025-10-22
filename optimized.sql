-- Optimized 
USE Assignment_2;


CREATE INDEX idx_books_author_id ON books(author_id);
CREATE INDEX idx_books_price ON books(price);
CREATE INDEX idx_books_id_price ON books(id, price);

EXPLAIN
WITH 
author_stats AS (
    SELECT 
        author_id,
        COUNT(*) AS book_count,
        MAX(price) AS max_price
    FROM books
    GROUP BY author_id
    HAVING COUNT(*) > 5
),
price_stats AS (
    SELECT AVG(price) AS avg_price
    FROM books
)
SELECT 
    b.id AS book_id,
    b.title AS book_title,
    b.year_published,
    b.price,
    a.id AS author_id,
    a.country,
    ast.book_count AS author_book_count,
    ps.avg_price AS avg_all_books_price,
    ast.max_price AS author_max_price
FROM books b
INNER JOIN author_stats ast ON b.author_id = ast.author_id
INNER JOIN authors a ON b.author_id = a.id
CROSS JOIN price_stats ps
WHERE 
    b.price > ps.avg_price
    AND b.id < 10000
ORDER BY 
    ast.book_count DESC,
    b.price DESC
LIMIT 50;

