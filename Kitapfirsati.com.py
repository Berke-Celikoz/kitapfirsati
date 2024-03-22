from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load the scraped data from the CSV file
df = pd.read_csv('scraped_data.csv')

@app.route('/')
def index():
    # Convert discount percentage column to numeric values
    df['Discount Percentage'] = df['Discount Percentage'].astype(float)
    
    # Sort the data by discount percentage in descending order
    df_sorted = df.sort_values(by='Discount Percentage', ascending=False)
    
    # Render the template with the sorted data
    return render_template('index.html', books=df_sorted.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)