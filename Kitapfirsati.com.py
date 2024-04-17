from flask import Flask, render_template, request, request
import pandas as pd

app = Flask(__name__)

# Load the scraped data from the CSV file
df = pd.read_csv('scraped_data.csv')

# Number of books per page
BOOKS_PER_PAGE = 20

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Category Pages
@app.route('/edebiyat')
def edebiyat():
    # Add logic to fetch and display literature books
    page = int(request.args.get('page', 1))
    
    # Convert discount percentage column to numeric values
    df['Discount Percentage'] = df['Discount Percentage'].astype(float)
    
    # Sort the data by discount percentage in descending order
    df_sorted = df.sort_values(by='Discount Percentage', ascending=False)
    
    # Calculate the start and end indices for pagination
    start_index = (page - 1) * BOOKS_PER_PAGE
    end_index = start_index + BOOKS_PER_PAGE
    
    # Get the data for the current page
    books_page = df_sorted.iloc[start_index:end_index]
    
    # Calculate total number of pages
    total_pages = -(-len(df_sorted) // BOOKS_PER_PAGE)  # Ceiling division
    
    return render_template('edebiyat.html', books=books_page.to_dict(orient='records'), page=page, total_pages=total_pages)

@app.route('/bilim')
def bilim():
    # Add logic to fetch and display science books
    return render_template('category.html', category='Bilim Kitapları')

@app.route('/cizgiromanlar')
def cizgiromanlar():
    # Add logic to fetch and display comic books
    return render_template('category.html', category='Çizgi Romanlar')

if __name__ == '__main__':
    app.run(debug=True)