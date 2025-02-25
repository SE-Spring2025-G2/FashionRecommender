from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Searchhistory
from . import db
from flask_login import login_required, current_user

searchhistorybp = Blueprint('searchhistory', __name__)

@searchhistorybp.route("/searchhistory", methods=["GET"])
@login_required
def search_history(userid = None):
    history_records = Searchhistory.query.all()

    

    searchhistory = []
    for record in history_records:
        # Convert search_term from string to dictionary
        parts = '\n'+record.search_terms
        parts = parts.split("\n-")[1:]  # Split based on " - "
        # print("herrrrrrrrrrrre",record.search_terms,'\n',parts, flush=True)
        search_dict = {}
        for part in parts:
            if ":" in part:  # Ensure it has key-value structure
                key, value = part.split(":")  
                search_dict[key.strip()] = value.strip()

        if "lowerBudget" in search_dict:
            if "upperBudget" in search_dict:
                search_dict["budget"] = f"Budget Range: {search_dict['lowerBudget']} - {search_dict['upperBudget']}"
                del search_dict["lowerBudget"]
                del search_dict["upperBudget"]
            else:
                search_dict["budget"] = f"Budget Range: {search_dict['lowerBudget']} - N/A"
                del search_dict["lowerBudget"]
        
        # Append processed data
        searchhistory.append({"search_terms": search_dict, "search_links": record.search_links, "date": record.date})

    return render_template("searchhistory.html", user=current_user, searchhistory=searchhistory, enumerate=enumerate)
    