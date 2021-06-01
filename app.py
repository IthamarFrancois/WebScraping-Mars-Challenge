

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars



#############################  Initialize Flask #############################

app = Flask(__name__, template_folder='templates')

## Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_App"
mongo = PyMongo(app)

##########################################################    FLASK / API Routes   ##########################################################


## Home Route for index.html Mongo render
@app.route("/")
def index():
    
    ScrapeData = mongo.db.MarsScrap.find_one()
    return render_template("index.html", ScrapeData = ScrapeData)


## Scrape Route to use scrape_mars function
@app.route("/scrape")
def scrape():
    
    ## Drop duplicates in collection
    mongo.db.MarsScrap.drop
    
    ## Collection initialize
    MarsScrap = mongo.db.MarsScrap
    
    ## Run the scrape function
    scrapedata = scrape_mars.scrape()
    
    
    ## Update the Mongo database using update and upsert=True
    MarsScrap.update({}, scrapedata, upsert=True)
    
    ## Redirect back to home page
    return redirect("/", code=302)
    #return redirect("/")
    

    

#############################  Flask End  #############################

if __name__ == "__main__":
    app.run(debug=True)

## ________________________________________ Ithamar Francois ______________________________________________________ ##
