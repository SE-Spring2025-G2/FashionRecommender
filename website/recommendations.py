import functools
import json
import os
import re
from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required, current_user
from google import genai
from . import contracts
from werkzeug.security import check_password_hash, generate_password_hash
from . import models
from datetime import datetime
from werkzeug.utils import secure_filename
from pathlib import Path
from . import helper, utils
from pydantic import BaseModel, TypeAdapter
from .models import Searchhistory
from . import db
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    from projectsecrets.gemini_secret import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

UPLOAD_FOLDER = os.path.abspath("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

recommendationsbp = Blueprint("recommendationsbp", __name__, url_prefix="/")

class GeminiQueryResponse(BaseModel):
    query: str
    color_palette: list[str]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_color_palette_response(text):
    try:
        # Extract JSON-like string using regex
        json_str = re.search(r'\[\[\[.*?\]\]\]', text, re.DOTALL).group()
        return json.loads(json_str)
    except (AttributeError, json.JSONDecodeError) as e:
        print(f"Error parsing color palette: {e}", flush=True)
        return []

@recommendationsbp.route("/recommendations", methods=["POST"])
@login_required
def get_recommendations():
    try:
        userid = current_user.id
        if not userid:
            return jsonify({
                "error": "User not logged in",
                "error_code": contracts.ErrorCodes.USER_NOT_LOGGED_IN
            }), 403

        user = models.User.query.get(userid)
        if not user:
            return jsonify({
                "error": "User not found",
                "error_code": contracts.ErrorCodes.USER_NOT_FOUND
            }), 404

        req_data = request.form
        if not req_data:
            return jsonify({
                "error": "Invalid request body",
                "error_code": contracts.ErrorCodes.INVALID_REQUEST
            }), 400

        user_filters = {
            "occasion": req_data.get(contracts.RecommendationContractRequest.OCCASION_KEY, ""),
            "gender": req_data.get(contracts.RecommendationContractRequest.GENDER_KEY, ""),
            "ageGroup": req_data.get(contracts.RecommendationContractRequest.AGE_GROUP_KEY, ""),
            "culture": req_data.get(contracts.RecommendationContractRequest.CULTURE_KEY, ""),
            "seasonalTrends": req_data.get(contracts.RecommendationContractRequest.SEASONAL_TRENDS_KEY, ""),
            "personalStyle": req_data.get(contracts.RecommendationContractRequest.PERSONAL_STYLE_KEY, ""),
            "bodyType": req_data.get(contracts.RecommendationContractRequest.BODY_TYPE_KEY, ""),
            "fitType": req_data.get(contracts.RecommendationContractRequest.FIT_TYPE_KEY, ""),
            "fabricPreference": req_data.get(contracts.RecommendationContractRequest.FABRICE_PREFERENCE_KEY, ""),
            "colorPreference": req_data.get(contracts.RecommendationContractRequest.COLOR_PREFERENCE_KEY, ""),
            "clothingType": req_data.get(contracts.RecommendationContractRequest.CLOTHING_TYPE_KEY, ""),
            "activityType": req_data.get(contracts.RecommendationContractRequest.ACTIVITY_TYPE_KEY, ""),
            "lowerBudget": req_data.get(contracts.RecommendationContractRequest.LOWER_BUDGET_KEY, ""),
            "upperBudget": req_data.get(contracts.RecommendationContractRequest.UPPER_BUDGET_KEY, ""),
        }

        filtered_filters = {key: value for key, value in user_filters.items() if value}
        filters_text = "\n".join([f"- {key}: {value}" for key, value in filtered_filters.items()])

        # print("here",filters_text)

        # # create a string with the values of the filtered_text
        # s = ''
        # for key, value in filtered_filters.items():
        #     s += f"{key}: {value},"
        # s = s.rstrip(',')
        # print(s)
        print("here",filters_text)

        # #jsonify the filtered_filters


        city = req_data.get(contracts.RecommendationContractRequest.CITY_KEY, "autodetect")
        if city == "autodetect" or city == "":
            city = utils.GeolocationAPI().getCurrentLocation()

        temperature_f, weather_condition = utils.WeatherAPI().getCurrentWeather(city=city)

        # Handle missing weather data
        weather_info = ""
        if weather_condition and temperature_f is not None:
            weather_info = f"\n- The user plans to wear this outfit in **{weather_condition}** weather with a temperature of **{temperature_f}°F**."

        help = helper.RecommendationHelper()

        if "clothingImage" in request.files and request.files["clothingImage"].filename:
            clothing_image = request.files["clothingImage"]
            temp_file_path = os.path.join(UPLOAD_FOLDER, clothing_image.filename)
            clothing_image.save(temp_file_path)

            clothing_file = client.files.upload(file=Path(temp_file_path))

            prompt = f"""
You are a **fashion recommendation AI**. Based on the **uploaded image** (which reflects the user's preferred style), the **selected filters**, and additional context, generate:
1. A **Google Image Search Query** that captures the **mood, color scheme, style, and dress theme** based on the user's chosen filters.
2. A **Recommended Color Palette** in `#rrggbb` format that complements the user's preferences and chosen filters.

### **User-Selected Filters:** 
{filters_text}
{f"Weather considerations: {weather_info}" if weather_info else ""}

### **Additional Context:**
- If weather details are provided, consider them while generating recommendations.
- Format the **Google Image Search Query** as a **concise and natural search phrase** that reflects real-world fashion search behavior. 
- Example Format: 
  - ✅ `"Elegant winter coat outfit for men in New York - modern style"`
  - ✅ `"Bohemian summer dress inspiration for women - vibrant colors"`
- Avoid:
  - ❌ `"Mens party outfit partly cloudy weather 57 degrees"`
- The **color palette should be a recommendation**, suggesting colors that best suit the user's selected filters and context.
"""
            print(f"Prompt: {prompt}", flush=True)

            result = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[clothing_file, prompt],
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': GeminiQueryResponse
                }
            )
            response: GeminiQueryResponse = result.parsed

            os.remove(temp_file_path)

            links = help.giveRecommendationsBasedOnGemini(response.query)

            return jsonify({
                contracts.RecommendationContractResponse.LINKS: links,
                "COLOR_PALETTES": response.color_palette
            }), 200
        else:
            print("No image file found", flush=True)
            prompt = f"""
You are a **fashion recommendation AI**. Based on the **selected filters** and additional context, generate:
1. A **Google Image Search Query** that captures the **mood, color scheme, style, and dress theme** based on the user's chosen filters.
2. A **Recommended Color Palette** in `#rrggbb` format that complements the user's preferences and chosen filters.

### **User-Selected Filters:**  
{filters_text}
{f"Weather considerations: {weather_info}" if weather_info else ""}

### **Additional Context:**
- If weather details are provided, consider them while generating recommendations.
- Format the **Google Image Search Query** as a **concise and natural search phrase** that reflects real-world fashion search behavior. 
- Example Format: 
  - ✅ `"Elegant winter coat outfit for men - modern style"`
  - ✅ `"Bohemian summer dress inspiration for women - vibrant colors"`
- Avoid:
  - ❌ `"Mens party outfit partly cloudy weather 57 degrees"`
- The **color palette should be a recommendation**, suggesting colors that best suit the user's selected filters and context.
"""
            
            print(f"Promptuu: {prompt}", flush=True)

            result = client.models.generate_content(
                contents=prompt,
                model="gemini-2.0-flash",
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': GeminiQueryResponse
                }
            )
            response: GeminiQueryResponse = result.parsed

            links = help.giveRecommendationsBasedOnGemini(response.query)
            print("length:", len(links))

            new_search_history = Searchhistory(search_terms = filters_text, search_links = links, userid = current_user.id)
            db.session.add(new_search_history)
            db.session.commit()

            return jsonify({
                contracts.RecommendationContractResponse.LINKS: links,
                "COLOR_PALETTES": response.color_palette
            }), 200

    except Exception as e:
        print(f"Server error: {str(e)}", flush=True)
        return jsonify({
            "error": "Internal server error",
            # "error_code": contracts.ErrorCodes.SERVER_ERROR
        }), 500

@recommendationsbp.route("/style_match", methods=["POST"])
def style_match():
    try:
        if "clothingImage" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        clothing_image = request.files["clothingImage"]

        if clothing_image.filename == "":
            return jsonify({"error": "No file selected"}), 400

        temp_file_path = os.path.join(UPLOAD_FOLDER, clothing_image.filename)
        clothing_image.save(temp_file_path)

        myfile = client.files.upload(file=Path(temp_file_path))

        prompt = """Based on the uploaded image, can you suggest clothing items or outfit recommendations in JSON format?
            Include the following keys:

            - 'recommended_outfits': A list of outfit ideas with their names and descriptions.
            - 'accessories': Suggested matching accessories with their types and color schemes.
            - 'recommended_outfits': A list of outfit ideas with their names and descriptions in form [{'name':name, 'description':description}, ...].
            - 'style_tips': Any additional styling tips or details."""

        result = client.models.generate_content(contents=[myfile, prompt], model="gemini-2.0-flash")
        response = result.text

        os.remove(temp_file_path)

        return jsonify({"recommendations": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
