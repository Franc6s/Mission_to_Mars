from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__, template_folder='templates')

# Use flask_pymongo to set up Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
