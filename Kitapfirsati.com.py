from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the scraped data from the CSV file
df = pd.read_csv('scraped_data.csv')

# Number of books per page
BOOKS_PER_PAGE = 20

@app.route('/')
def index():
    # Get page number from query string, default to 1 if not provided
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
    
    # Render the template with the data for the current page and pagination info
    return render_template('index.html', books=books_page.to_dict(orient='records'), page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)