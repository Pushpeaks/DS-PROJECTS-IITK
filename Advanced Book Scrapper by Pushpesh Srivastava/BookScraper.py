import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import time
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/catalogue/"

def get_soup(url):
    """Fetches the page content and returns a BeautifulSoup object."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def get_book_links(page_url):
    """Extracts all book links from a category page."""
    soup = get_soup(page_url)
    if not soup:
        return []
    book_links = []
    link_elements = soup.select('article.product_pod h3 a')
    for link_element in link_elements:
        rel_url = link_element.get('href')
        full_url = urljoin(BASE_URL, rel_url)
        book_links.append(full_url)
    return book_links

def parse_book_page(book_url):
    """Parses a single book page and returns a dictionary of book details."""
    soup = get_soup(book_url)
    if not soup:
        return None

    try:
        title = soup.h1.text.strip()
        price = soup.select_one("p.price_color").text.strip()
        availability = soup.select_one("p.instock.availability").text.strip()
        
        # Scrape star rating (e.g., "star-rating One")
        rating_element = soup.select_one("p.star-rating")
        rating = rating_element['class'][1] if rating_element else "No Rating"

        description_div = soup.select_one("div#product_description")
        description_text = ""
        if description_div:
            # The description is in the <p> sibling of the <div>
            description_text = description_div.find_next_sibling("p").text.strip()
        else:
            description_text = "No Description"

        # The category is the second last item in the breadcrumb
        breadcrumb = soup.select('ul.breadcrumb li a')
        category = breadcrumb[-2].text.strip() if len(breadcrumb) > 1 else "No Category"

        return {
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating,
            'Description': description_text,
            'Category': category,
            'URL': book_url
        }
    except Exception as e:
        print(f"Error parsing book page {book_url}: {e}")
        return None

def scrap_all_books(limit_pages=5):
    """Scrapes a specified number of pages and returns a list of book dictionaries."""
    all_books_dict = []
    print(f"Scraping {limit_pages} pages in progress...")
    for i in range(1, limit_pages + 1):
        page_url = f"https://books.toscrape.com/catalogue/page-{i}.html"
        book_links = get_book_links(page_url)
        for desc_link in book_links:
            book_detail = parse_book_page(desc_link)
            if book_detail:
                all_books_dict.append(book_detail)
            time.sleep(0.5)  # Be polite to the server
    print("Scraping complete.")
    return all_books_dict

def save_to_csv(books, filename="books.csv"):
    """Saves a list of book dictionaries to a CSV file."""
    if not books:
        print("No books to save.")
        return

    fieldnames = list(books[0].keys())
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)
    print(f"Data saved to {filename}")

def save_to_db(books, dbname="books.db"):
    """Saves a list of book dictionaries to an SQLite database."""
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    
    # Create the table if it doesn't exist
    qry = '''CREATE TABLE IF NOT EXISTS books (
        title TEXT,
        price TEXT,
        availability TEXT,
        rating TEXT,
        description TEXT,
        category TEXT,
        url TEXT
    )'''
    cur.execute(qry)
    
    # Clear existing data
    cur.execute("DELETE FROM books")
    conn.commit()

    # Insert new data
    for book in books:
        cur.execute('''
            INSERT INTO books (title, price, availability, rating, description, category, url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            book['Title'],
            book['Price'],
            book['Availability'],
            book['Rating'],
            book['Description'],
            book['Category'],
            book['URL']
        ))
    
    conn.commit()
    conn.close()
    print(f"Data saved to {dbname}")

if __name__ == "__main__":
    scraped_books = scrap_all_books(limit_pages=5)
    if scraped_books:
        save_to_csv(scraped_books)
        save_to_db(scraped_books)