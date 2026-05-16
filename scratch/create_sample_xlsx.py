import pandas as pd

data = [
    # customers
    ["customers", "Show me all customers from the state of Sao Paulo.", "SELECT * FROM customers WHERE customer_state = 'SP';"],
    ["customers", "How many unique customers are registered in the city of Curitiba?", "SELECT COUNT(DISTINCT customer_unique_id) FROM customers WHERE customer_city = 'curitiba';"],
    ["customers", "Find the customer ID for the person with unique ID '861eff4711a542e4b93843c6dd7febb0'.", "SELECT customer_id FROM customers WHERE customer_unique_id = '861eff4711a542e4b93843c6dd7febb0';"],
    
    # geolocation
    ["geolocation", "Get the latitude and longitude for the zip code 1037.", "SELECT geolocation_lat, geolocation_lng FROM geolocation WHERE geolocation_zip_code_prefix = 1037;"],
    ["geolocation", "List all unique cities in the state of Rio de Janeiro.", "SELECT DISTINCT geolocation_city FROM geolocation WHERE geolocation_state = 'RJ';"],
    ["geolocation", "Find the average latitude of all registered locations in Brazil.", "SELECT AVG(geolocation_lat) FROM geolocation;"],
    
    # order_items
    ["order_items", "What is the total price for order '00010242fe8c5a6d1ba2dd792cb16214'?", "SELECT SUM(price) FROM order_items WHERE order_id = '00010242fe8c5a6d1ba2dd792cb16214';"],
    ["order_items", "Show me the top 5 most expensive items sold.", "SELECT * FROM order_items ORDER BY price DESC LIMIT 5;"],
    ["order_items", "How many items were sold by seller '48436dade18ac8b2bce089ec2a041202'?", "SELECT COUNT(*) FROM order_items WHERE seller_id = '48436dade18ac8b2bce089ec2a041202';"],
    
    # order_payments
    ["order_payments", "Show all payment methods used for order 'b81ef226f3fe1789b1e8b2acac839d17'.", "SELECT payment_type FROM order_payments WHERE order_id = 'b81ef226f3fe1789b1e8b2acac839d17';"],
    ["order_payments", "What is the total value paid across all orders using credit cards?", "SELECT SUM(payment_value) FROM order_payments WHERE payment_type = 'credit_card';"],
    ["order_payments", "Find orders that were paid in more than 10 installments.", "SELECT DISTINCT order_id FROM order_payments WHERE payment_installments > 10;"],
    
    # order_reviews
    ["order_reviews", "List all reviews with a score of 1 (worst).", "SELECT * FROM order_reviews WHERE review_score = 1;"],
    ["order_reviews", "Show me the comments for order '73fc7af87114b39712e6da79b0a377eb'.", "SELECT review_comment_message FROM order_reviews WHERE order_id = '73fc7af87114b39712e6da79b0a377eb';"],
    ["order_reviews", "What is the average review score for all orders?", "SELECT AVG(review_score) FROM order_reviews;"],
    
    # orders
    ["orders", "How many orders are currently in 'delivered' status?", "SELECT COUNT(*) FROM orders WHERE order_status = 'delivered';"],
    ["orders", "Find all orders placed in October 2017.", "SELECT * FROM orders WHERE order_purchase_timestamp LIKE '2017-10%';"],
    ["orders", "Which orders were delivered later than their estimated delivery date?", "SELECT order_id FROM orders WHERE order_delivered_customer_date > order_estimated_delivery_date;"],
    
    # product_category_name_translation
    ["product_category_name_translation", "What is the English translation for the category 'beleza_saude'?", "SELECT product_category_name_english FROM product_category_name_translation WHERE product_category_name = 'beleza_saude';"],
    ["product_category_name_translation", "List all Portuguese category names that contain the word 'informatica'.", "SELECT product_category_name FROM product_category_name_translation WHERE product_category_name LIKE '%informatica%';"],
    ["product_category_name_translation", "Show all category translations available.", "SELECT * FROM product_category_name_translation;"],
    
    # products
    ["products", "Show me all products in the 'perfumaria' category.", "SELECT * FROM products WHERE product_category_name = 'perfumaria';"],
    ["products", "Find products that have more than 5 photos.", "SELECT product_id FROM products WHERE product_photos_qty > 5;"],
    ["products", "What is the average weight (in grams) of products in the database?", "SELECT AVG(product_weight_g) FROM products;"],
    
    # sellers
    ["sellers", "List all sellers located in the city of 'campinas'.", "SELECT * FROM sellers WHERE seller_city = 'campinas';"],
    ["sellers", "How many sellers are registered in the state of Minas Gerais (MG)?", "SELECT COUNT(*) FROM sellers WHERE seller_state = 'MG';"],
    ["sellers", "Find the zip code prefix for seller '3442f8959a84dea7ee197c632cb2df15'.", "SELECT seller_zip_code_prefix FROM sellers WHERE seller_id = '3442f8959a84dea7ee197c632cb2df15';"],
]

df = pd.DataFrame(data, columns=["table_name", "query", "sql"])
output_path = r"c:\Users\thoma\SynologyDrive\Coding\text_to_sql\scratch\sample_queries.xlsx"
df.to_excel(output_path, index=False)
print(f"File saved to {output_path}")
