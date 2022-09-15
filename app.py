#import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#app
app = Flask(__name__)

#connect to mongodb
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#route
@app.route("/")
def index():
    #find one doc in mongoDB & return
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)

#path to scrape
@app.route("/scrape")
def scraper():
    mars_info = mongo.db.mars_info 
    mars_info_data = scrape_mars.scrape()
    mars_info.update_many({}, {"$set": mars_info_data}, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)