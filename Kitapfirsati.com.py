from flask import Flask, render_template, request, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('scraped_data.csv')

BOOKS_PER_PAGE = 24

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/book/<unique_id>')
def book_details(unique_id):
    # Check if the unique_id exists in the DataFrame
    if unique_id in df["Unique ID"].values:
        # Fetch the book data for the given unique_id
        book = df[df["Unique ID"] == unique_id].iloc[0].to_dict()
        return render_template('book_details.html', book=book)
    else:
        # If the book with the given unique_id is not found, render a custom not found page
        return render_template('not_found.html'), 404

@app.route('/edebiyat')
def edebiyat():
    page = int(request.args.get('page', 1))
    
    df['Discount Percentage'] = df['Discount Percentage'].astype(float)
    
    df_sorted = df.sort_values(by='Discount Percentage', ascending=False)
    
    start_index = (page - 1) * BOOKS_PER_PAGE
    end_index = start_index + BOOKS_PER_PAGE
    
    books_page = df_sorted.iloc[start_index:end_index]
    
    total_pages = -(-len(df_sorted) // BOOKS_PER_PAGE) 
    
    return render_template('edebiyat.html', books=books_page.to_dict(orient='records'), page=page, total_pages=total_pages)

@app.route('/bilim')
def bilim():
    return render_template('category.html', category='Bilim Kitapları')

@app.route('/cizgiromanlar')
def cizgiromanlar():
    return render_template('category.html', category='Çizgi Romanlar')

if __name__ == '__main__':
    app.run(debug=True)