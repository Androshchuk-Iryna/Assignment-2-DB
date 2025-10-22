-- Non-optimized (AI-generated)

EXPLAIN 
SELECT 
    b.id AS book_id,
    b.title AS book_title,
    b.year_published,
    b.price,
    a.id AS author_id,
    a.name AS author_name,
    a.country,
    
    (SELECT COUNT(*) 
     FROM books b2 
     WHERE b2.author_id = a.id) AS author_book_count,
    
    (SELECT AVG(price) 
     FROM books) AS avg_all_books_price,
    
    (SELECT MAX(price) 
     FROM books b3 
     WHERE b3.author_id = a.id) AS author_max_price

FROM books b
JOIN authors a ON b.author_id = a.id

WHERE 
    b.price > (SELECT AVG(price) FROM books)
    
    AND a.id IN (
        SELECT author_id 
        FROM books 
        GROUP BY author_id 
        HAVING COUNT(*) > 5
    )
    
    AND b.id < 10000

ORDER BY 
    (SELECT COUNT(*) FROM books b4 WHERE b4.author_id = a.id) DESC,
    b.price DESC
    
LIMIT 50;
