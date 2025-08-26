import pandas as pd
import re
from collections import Counter

# Step 1: Load Data and Clean
df = pd.read_csv("books.csv")
df['Price'] = df['Price'].str.replace('£', '').astype(float)
df['Availability'] = df['Availability'].str.extract('(\d+)').astype(int)

# Normalize the 'Rating' column to be consistent (e.g., 'One' -> 1)
rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
df['Rating'] = df['Rating'].map(rating_map).fillna(0).astype(int)

print("Data loaded and cleaned successfully.\n" + "="*50)

# --- Pandas Queries ---

# 1. Convert Price from string to float (Already done in the setup)
print("1. Price column converted to float.")

# 2. Top 5 most expensive books
print("\n2. Top 5 most expensive books:")
print(df.nlargest(5, 'Price')[['Title', 'Price']])

# 3. Average price of all books
print(f"\n3. Average price of all books: £{df['Price'].mean():.2f}")

# 4. Count of books by star rating
print("\n4. Count of books by star rating:")
print(df['Rating'].value_counts().sort_index())

# 5. Number of books in each category
print("\n5. Number of books in each category:")
print(df['Category'].value_counts())

# 6. Books with "Python" in the title
print("\n6. Books with 'Python' in the title:")
print(df[df['Title'].str.contains('python', case=False, na=False)][['Title', 'Category']])

# 7. Books currently in stock
print("\n7. Books currently in stock:")
print(df[df['Availability'] > 0][['Title', 'Availability']])

# 8. Out-of-stock books
print("\n8. Out-of-stock books:")
print(df[df['Availability'] == 0][['Title', 'Availability']])

# 9. Count of books missing a description
print(f"\n9. Count of books missing a description: {df['Description'].isna().sum()}")

# 10. Most common book rating
most_common_rating = df['Rating'].mode()[0]
print(f"\n10. Most common book rating: {most_common_rating} star(s)")

# 11. Number of unique categories
print(f"\n11. Number of unique categories: {df['Category'].nunique()}")

# 12. List all unique categories
print("\n12. List all unique categories:")
print(df['Category'].unique())

# 13. Sort all books alphabetically by title
print("\n13. First 10 books sorted alphabetically by title:")
print(df.sort_values('Title')[['Title']].head(10))

# 14. Books with the longest descriptions
df['Description_Length'] = df['Description'].str.len()
print("\n14. Top 5 books with the longest descriptions:")
print(df.nlargest(5, 'Description_Length')[['Title', 'Description_Length']])
df.drop('Description_Length', axis=1, inplace=True)

# 15. Cheapest book in each category
print("\n15. Cheapest book in each category:")
print(df.loc[df.groupby('Category')['Price'].idxmin()][['Category', 'Title', 'Price']])

# 16. Top 3 most expensive books per category
print("\n16. Top 3 most expensive books per category:")
print(df.groupby('Category').apply(lambda x: x.nlargest(3, 'Price'))[['Title', 'Price']].droplevel(0))

# 17. Books with title length > 50 characters
df['Title_Length'] = df['Title'].str.len()
print("\n17. Books with title length > 50 characters:")
print(df[df['Title_Length'] > 50][['Title', 'Title_Length']])
df.drop('Title_Length', axis=1, inplace=True)

# 18. Add a column for "is_expensive" (price > £40)
df['is_expensive'] = df['Price'] > 40
print("\n18. Count of expensive books (price > £40):")
print(df['is_expensive'].value_counts())

# 19. Average price of expensive books
print(f"\n19. Average price of expensive books: £{df[df['is_expensive']]['Price'].mean():.2f}")

# 20. Books with a 5-star rating
print("\n20. Books with a 5-star rating:")
print(df[df['Rating'] == 5][['Title', 'Rating']])

# 21. Books with multiple copies in stock
print("\n21. Books with multiple copies in stock:")
print(df[df['Availability'] > 1][['Title', 'Availability']])

# 22. Category with the lowest average price
avg_price_by_cat = df.groupby('Category')['Price'].mean()
lowest_avg_price_cat = avg_price_by_cat.idxmin()
print(f"\n22. Category with the lowest average price: {lowest_avg_price_cat} (Average Price: £{avg_price_by_cat.min():.2f})")

# 23. How many books have 5-star ratings
print(f"\n23. Number of books with 5-star ratings: {len(df[df['Rating'] == 5])}")

# 24. List all 5-star books priced above £50
print("\n24. 5-star books priced above £50:")
print(df[(df['Rating'] == 5) & (df['Price'] > 50)][['Title', 'Price', 'Rating']])

# 25. What is the average price of 1-star books?
print(f"\n25. Average price of 1-star books: £{df[df['Rating'] == 1]['Price'].mean():.2f}")

# 26. Top 10 categories with the most in-stock books
print("\n26. Top 10 categories with the most in-stock books:")
print(df.groupby('Category')['Availability'].sum().nlargest(10))

# 27. Which books are completely out of stock?
print("\n27. Books completely out of stock:")
print(df[df['Availability'] == 0][['Title', 'Availability']])

# 28. Books with descriptions containing the word "mystery"
print("\n28. Books with descriptions containing the word 'mystery':")
print(df[df['Description'].str.contains('mystery', case=False, na=False)][['Title']])

# 29. Book with the highest price in the entire dataset
highest_price_book = df.loc[df['Price'].idxmax()]
print(f"\n29. Book with the highest price: {highest_price_book['Title']} (Price: £{highest_price_book['Price']})")

# 30. Book with the lowest price
lowest_price_book = df.loc[df['Price'].idxmin()]
print(f"\n30. Book with the lowest price: {lowest_price_book['Title']} (Price: £{lowest_price_book['Price']})")

# 31. How many books are priced exactly at £50?
print(f"\n31. Number of books priced exactly at £50: {len(df[df['Price'] == 50])}")

# 32. Rank books by price within each category
print("\n32. First 10 books ranked by price within each category:")
df['Rank_by_Price_in_Category'] = df.groupby('Category')['Price'].rank(ascending=False, method='min')
print(df.sort_values(['Category', 'Rank_by_Price_in_Category'])[['Category', 'Title', 'Price', 'Rank_by_Price_in_Category']].head(10))

# 33. Books with a title starting with 'A'
print("\n33. Books with a title starting with 'A':")
print(df[df['Title'].str.startswith('A')][['Title']])

# 34. Average title length per category
df['Title_Length'] = df['Title'].str.len()
print("\n34. Average title length per category:")
print(df.groupby('Category')['Title_Length'].mean())
df.drop('Title_Length', axis=1, inplace=True)

# 35. Most common word in all titles
all_titles = ' '.join(df['Title'].values).lower()
words = re.findall(r'\b\w+\b', all_titles)
most_common_word = Counter(words).most_common(1)
print(f"\n35. Most common word in all titles: {most_common_word[0][0]} (Count: {most_common_word[0][1]})")

# 36. Books with descriptions longer than 300 characters
df['Description_Length'] = df['Description'].str.len()
print("\n36. Books with descriptions longer than 300 characters:")
print(df[df['Description_Length'] > 300][['Title', 'Description_Length']])
df.drop('Description_Length', axis=1, inplace=True)

# 37. Distribution of books by rating and category
print("\n37. Distribution of books by rating and category:")
print(df.groupby(['Category', 'Rating'])['Title'].count().unstack(fill_value=0))

# 38. Remove duplicate titles
# Note: The scraped dataset from the first 5 pages doesn't have duplicates, but here is the code.
df_no_duplicates = df.drop_duplicates(subset='Title', keep='first')
print(f"\n38. Original number of books: {len(df)}, Books after removing duplicate titles: {len(df_no_duplicates)}")

# 39. Find books priced below category average
category_avg_prices = df.groupby('Category')['Price'].transform('mean')
books_below_avg = df[df['Price'] < category_avg_prices]
print("\n39. First 10 books priced below their category average:")
print(books_below_avg[['Title', 'Category', 'Price']].head(10))

# 40. Pivot table of average price per category and rating
print("\n40. Pivot table of average price per category and rating:")
pivot_table = df.pivot_table(values='Price', index='Category', columns='Rating', aggfunc='mean')
print(pivot_table)