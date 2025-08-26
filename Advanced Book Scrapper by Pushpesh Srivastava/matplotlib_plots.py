import pandas as pd
import matplotlib.pyplot as plt
import os

# Create a directory to save the plots
if not os.path.exists('plots'):
    os.makedirs('plots')

# Load and clean data
try:
    df = pd.read_csv("books.csv")
    df['Price'] = df['Price'].str.replace('£', '').astype(float)
    df['Availability'] = df['Availability'].str.extract('(\d+)').astype(int)
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['Rating'] = df['Rating'].map(rating_map).fillna(0).astype(int)
except FileNotFoundError:
    print("Error: 'books.csv' not found. Please run the scraping script first.")
    exit()

# 1. Average Price per Category
avg_price_cat = df.groupby('Category')['Price'].mean().sort_values(ascending=False)
plt.figure(figsize=(15, 8))
avg_price_cat.plot(kind='bar', color='skyblue')
plt.title('Average Price per Category')
plt.xlabel('Category')
plt.ylabel('Average Price (£)')
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.savefig('plots/1_avg_price_per_category.png')
plt.close()

# 2. Number of Books by Rating
books_by_rating = df['Rating'].value_counts().sort_index()
plt.figure(figsize=(8, 6))
books_by_rating.plot(kind='bar', color='lightcoral')
plt.title('Number of Books by Star Rating')
plt.xlabel('Star Rating')
plt.ylabel('Number of Books')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('plots/2_books_by_rating.png')
plt.close()

# 3. Books in Stock vs Out of Stock
in_stock = df[df['Availability'] > 0].shape[0]
out_of_stock = df[df['Availability'] == 0].shape[0]
stock_counts = pd.Series([in_stock, out_of_stock], index=['In Stock', 'Out of Stock'])
plt.figure(figsize=(6, 6))
stock_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'salmon'], startangle=90)
plt.title('Books in Stock vs Out of Stock')
plt.ylabel('')
plt.tight_layout()
plt.savefig('plots/3_stock_distribution.png')
plt.close()

# 4. Top 10 Most Expensive Books
top_10_expensive = df.nlargest(10, 'Price')[['Title', 'Price']]
plt.figure(figsize=(12, 8))
plt.barh(top_10_expensive['Title'], top_10_expensive['Price'], color='purple')
plt.title('Top 10 Most Expensive Books')
plt.xlabel('Price (£)')
plt.ylabel('Book Title')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('plots/4_top_10_expensive_books.png')
plt.close()

# 5. Book Count by Category (Top 10)
book_counts_cat = df['Category'].value_counts().nlargest(10)
plt.figure(figsize=(15, 8))
book_counts_cat.plot(kind='bar', color='darkcyan')
plt.title('Top 10 Categories by Book Count')
plt.xlabel('Category')
plt.ylabel('Number of Books')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('plots/5_top_10_categories.png')
plt.close()

# 6. Distribution of Book Prices (Histogram)
plt.figure(figsize=(10, 6))
df['Price'].plot(kind='hist', bins=20, color='royalblue', edgecolor='black')
plt.title('Distribution of Book Prices')
plt.xlabel('Price (£)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('plots/6_price_distribution.png')
plt.close()

# 7. Title Length Distribution
df['Title_Length'] = df['Title'].str.len()
plt.figure(figsize=(10, 6))
df['Title_Length'].plot(kind='hist', bins=20, color='orange', edgecolor='black')
plt.title('Distribution of Book Title Lengths')
plt.xlabel('Title Length (Characters)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('plots/7_title_length_distribution.png')
plt.close()

# 8. Boxplot of Prices by Rating
plt.figure(figsize=(10, 6))
df.boxplot(column='Price', by='Rating', grid=False)
plt.title('Boxplot of Prices by Rating')
plt.suptitle('')
plt.xlabel('Star Rating')
plt.ylabel('Price (£)')
plt.tight_layout()
plt.savefig('plots/8_price_by_rating_boxplot.png')
plt.close()

# 9. Number of Books Over Price Thresholds
thresholds = [10, 20, 30, 40, 50, 60]
counts = [len(df[df['Price'] > t]) for t in thresholds]
plt.figure(figsize=(10, 6))
plt.bar([f'>£{t}' for t in thresholds], counts, color='teal')
plt.title('Number of Books Over Price Thresholds')
plt.xlabel('Price Threshold')
plt.ylabel('Number of Books')
plt.tight_layout()
plt.savefig('plots/9_price_thresholds.png')
plt.close()

# 10. Top Categories with Most 5-Star Books
five_star_books = df[df['Rating'] == 5]
top_5_star_cats = five_star_books['Category'].value_counts().nlargest(10)
plt.figure(figsize=(15, 8))
top_5_star_cats.plot(kind='bar', color='gold', edgecolor='black')
plt.title('Top 10 Categories with the Most 5-Star Books')
plt.xlabel('Category')
plt.ylabel('Number of 5-Star Books')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('plots/10_top_5_star_categories.png')
plt.close()

print("All plots have been generated and saved in the 'plots' directory.")