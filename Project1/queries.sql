/*QUESTION 1*/
SELECT DISTINCT  f_query.title as movie, f_query.category,COUNT(f_query.title) OVER (PARTITION BY f_query.title)
FROM
(SELECT title,
c.name category
FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id
JOIN film f
ON fc.film_id = f.film_id
JOIN inventory iv
ON iv.film_id = f.film_id
JOIN rental r
ON r.inventory_id = iv.inventory_id
WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family','Music') )f_query
ORDER BY 2,1;

/*QUESTION 2*/
SELECT title, category, rental_duration, NTILE(4) OVER (ORDER BY rental_duration) AS standard_quartile
FROM(
SELECT DISTINCT title ,c.name AS category,rental_duration
FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id
JOIN film f
ON fc.film_id = f.film_id
JOIN inventory iv
ON iv.film_id = f.film_id
JOIN rental r
ON r.inventory_id = iv.inventory_id
WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family','Music')) s_query;

/*QUESTION 3*/

SELECT s_2_query.category,s_2_query.standard_quartile,COUNT(s_2_query.standard_quartile) AS count
FROM
(SELECT title, category, rental_duration, NTILE(4) OVER (ORDER BY rental_duration) AS standard_quartile
FROM(
SELECT DISTINCT title ,c.name AS category,rental_duration
FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id
JOIN film f
ON fc.film_id = f.film_id
JOIN inventory iv
ON iv.film_id = f.film_id
JOIN rental r
ON r.inventory_id = iv.inventory_id
WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family','Music')) s_query) s_2_query
  GROUP BY 1,2
  ORDER BY 1,2;


/*QUESTION 4*/
WITH f_query AS
(SELECT DATE_PART('month',rental_date) rental_month,DATE_PART('year',rental_date) rental_day, s.store_id store_id
FROM rental r
JOIN staff s
ON r.staff_id = s.staff_id
JOIN store st
ON st.store_id = s.store_id)

SELECT rental_month,rental_day, store_id,COUNT(rental_month) count
FROM f_query
GROUP BY 1,2,3
ORDER BY 4 DESC
