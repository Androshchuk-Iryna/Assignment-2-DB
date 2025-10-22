# Assignment-2-DB(Optimization)


## results

| Metric | Before Optimization | After Optimization | Improvement |
|--------|--------------------|--------------------|-------------|
| **Execution Time** | 6.157 sec | 1.643 sec | **3.75x faster** ⚡ |


---

## Optimization Steps

### 1. Created Indexes
```sql
CREATE INDEX idx_books_author_id ON books(author_id);
CREATE INDEX idx_books_price ON books(price);
CREATE INDEX idx_books_id_price ON books(id, price);
```
---

### 2. Replaced Subqueries with CTEs

**Before:**
```sql
SELECT 
    (SELECT COUNT(*) FROM books b2 WHERE b2.author_id = a.id) AS author_book_count,
    (SELECT AVG(price) FROM books) AS avg_all_books_price
FROM books b
JOIN authors a ON b.author_id = a.id;
```

**After:**
```sql
WITH 
author_stats AS (
    SELECT author_id, COUNT(*) AS book_count
    FROM books
    GROUP BY author_id
    HAVING COUNT(*) > 5
),
price_stats AS (
    SELECT AVG(price) AS avg_price
    FROM books
)
SELECT 
    ast.book_count AS author_book_count,
    ps.avg_price AS avg_all_books_price
FROM books b
INNER JOIN author_stats ast ON b.author_id = ast.author_id
CROSS JOIN price_stats ps;
```

---

### 3. Replaced IN Subquery with INNER JOIN

**Before:**
```sql
WHERE a.id IN (
    SELECT author_id 
    FROM books 
    GROUP BY author_id 
    HAVING COUNT(*) > 5
)
```

**After:**
```sql
INNER JOIN author_stats ast ON b.author_id = ast.author_id
-- author_stats already contains only authors with >5 books
```

Faster table joining using indexes (hash join instead of nested loop).

---

### 4. Used Pre-calculated Values for ORDER BY

**Before:**
```sql
ORDER BY 
    (SELECT COUNT(*) FROM books b4 WHERE b4.author_id = a.id) DESC,
    b.price DESC
```

**After:**
```sql
ORDER BY 
    ast.book_count DESC,  -- Pre-calculated in CTE
    b.price DESC
```


---


### Before Optimization

<img width="1115" height="172" alt="Знімок екрана 2025-10-22 о 18 52 29" src="https://github.com/user-attachments/assets/8cb3a45f-81bb-4448-ad45-ffe684d27366" />


**Problems:**
- `DEPENDENT SUBQUERY` — Executes multiple times
- `Using temporary; Using filesort` — Slow sorting
- No indexes used

---

### After Optimization
<img width="1112" height="139" alt="Знімок екрана 2025-10-22 о 18 50 43" src="https://github.com/user-attachments/assets/81e17374-fcd5-4dac-8310-7c30966b87bb" />
- `DERIVED` — CTE materialized once
- `Using index` — Covering index (no table access)

Out put 
<img width="1043" height="226" alt="Знімок екрана 2025-10-22 о 18 55 59" src="https://github.com/user-attachments/assets/be903345-2004-40a2-9210-4a30c1293bf3" />


AI usage 
https://claude.ai/share/cd036e85-2862-4732-8403-a437966a38ff 
