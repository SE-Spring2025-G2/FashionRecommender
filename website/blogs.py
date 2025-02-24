from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session
)

from flask_login import current_user, login_required

import requests
from bs4 import BeautifulSoup

blogsbp = Blueprint("blogs", __name__)
@blogsbp.route("/blogs", methods=["GET"])
@login_required
# List of websites


def blogs():
    
    

    # URL of the fashion blogs page
    URL = "https://detailed.com/fashion-blogs/"

    # Headers to mimic a browser request
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Fetch the webpage
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print("Failed to fetch the page.")
        exit()

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract blog elements
    blogs = []
    for row in soup.find_all("tr", class_="photography-wrapper"):
        name = row.find("h3").text.strip()
        url = row.find("a")["href"].strip()
        text = row.find("span", class_="blog-description").text.strip()
        image = row.find("img")["src"].strip()

        blogs.append({
            "Name": name,
            "URL": url,
            "Text": text,
            "Image": image
        })

    


    return render_template("blogs.html",user=current_user, blogs=blogs, enumerate=enumerate)