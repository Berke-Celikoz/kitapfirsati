from flask import Flask, render_template, request, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('scraped_data.csv')

BOOKS_PER_PAGE = 20

@app.route('/')
def home():
    return render_template('home.html')

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