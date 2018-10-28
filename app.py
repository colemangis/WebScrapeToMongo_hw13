# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/weather_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    marsData = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", marsData=marsData)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    mars_listings = scrape_mars.scrape()


    # Store results into a dictionary
    marsData = {
        "nasa_title": mars_listings["nasa_title"],
        "nasa_teaser": mars_listings["nasa_teaser"],
        "featured_image_url": mars_listings["featured_image_url"],
        "weather": mars_listings["weather"],
        "mars_html": mars_listings["mars_html"],
        "hemisphere_image_urls": mars_listings["hemisphere_image_urls"],
    }

    # Insert forecast into database
    mongo.db.collection.insert_one(marsData)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
