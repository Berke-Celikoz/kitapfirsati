from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
BOOKS_PER_PAGE = 20
# Load the scraped data from the CSV file
df = pd.read_csv('scraped_data.csv')

@app.route('/')
@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    start_idx = (page - 1) * BOOKS_PER_PAGE
    end_idx = start_idx + BOOKS_PER_PAGE

    # Convert discount percentage column to numeric values
    df['Discount Percentage'] = df['Discount Percentage'].astype(float)
    
    # Sort the data by discount percentage in descending order
    df_sorted = df.sort_values(by='Discount Percentage', ascending=False)
    books_for_page = df_sorted.iloc[start_idx:end_idx].to_dict(orient='records')
    # Pass BOOKS_PER_PAGE to the template
    return render_template('index.html', books=books_for_page, page=page, BOOKS_PER_PAGE=BOOKS_PER_PAGE)

if __name__ == '__main__':
    app.run(debug=True)