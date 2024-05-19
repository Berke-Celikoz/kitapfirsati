from flask import Flask, render_template, request, redirect, session, flash
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

client = pymongo.MongoClient()
db = client["KitapfirsatiDB"]

df = pd.read_csv('scraped_data.csv')

BOOKS_PER_PAGE = 24

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/book/<unique_id>')
def book_details(unique_id):
    
    if unique_id in df["Unique ID"].values:
        
        book = df[df["Unique ID"] == unique_id].iloc[0].to_dict()
        return render_template('book_details.html', book=book)
    else:
        
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

@app.route('/uye-ol', methods=["GET", "POST"])
def uye_ol():
    if request.method == 'GET':
        return render_template("uye-ol.html")
    else:
        
        email = request.form["email"]
        sifre = request.form["sifre"]
        adsoyad = request.form["adsoyad"]

        
        hashed_sifre = generate_password_hash(sifre)

        try:
            
            db["kullanicilar"].insert_one({
                "_id": email,
                "sifre": hashed_sifre,
                "adsoyad": adsoyad
            })
            flash('Registration successful!', 'success')
            return redirect("/giris", 302)
        except pymongo.errors.DuplicateKeyError:
            flash('Email already exists!', 'danger')
            return redirect("/uye-ol", 302)

@app.route('/giris', methods=["GET", "POST"])
def giris():
    if request.method == 'GET':
        return render_template("giris.html")
    else:
        
        email = request.form["email"]
        sifre = request.form["sifre"]

        kullanici = db["kullanicilar"].find_one({"_id": email})
        if kullanici and check_password_hash(kullanici["sifre"], sifre):
            session['kullanici'] = kullanici
            flash('Login successful!', 'success')
            return redirect("/", 302)
        else:
            flash('Invalid email or password!', 'danger')
            return redirect("/giris", 302)

@app.route('/profile')
def profile():
    if 'kullanici' in session:
        return render_template('profile.html')
    else:
        flash('You need to be logged in to view this page.', 'danger')
        return redirect("/giris")

@app.route('/logout')
def logout():
    session.pop('kullanici', None)
    flash('You have been logged out.', 'success')
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)