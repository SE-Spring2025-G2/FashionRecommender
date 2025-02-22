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
import google.generativeai as genai
from . import contracts
from werkzeug.security import check_password_hash, generate_password_hash
from . import models
from datetime import datetime
from werkzeug.utils import secure_filename
from pathlib import Path

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    from projectsecrets.gemini_secret import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

UPLOAD_FOLDER = os.path.abspath("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

recommendationsbp = Blueprint("recommendationsbp", __name__, url_prefix="/")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_color_palette_response(text):
    try:
        # Extract JSON-like string using regex
        json_str = re.search(r'\[\[\[.*?\]\]\]', text, re.DOTALL).group()
        return json.loads(json_str)
    except (AttributeError, json.JSONDecodeError) as e:
        print(f"Error parsing color palette: {e}")
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

        req_data = request.get_json()
        if not req_data:
            return jsonify({
                "error": "Invalid request body",
                "error_code": contracts.ErrorCodes.INVALID_REQUEST
            }), 400

        culture = req_data.get(contracts.RecommendationContractRequest.CULTURE_KEY, "")
        occasion = req_data.get(contracts.RecommendationContractRequest.OCCASION_KEY, "")
        gender = req_data.get(contracts.RecommendationContractRequest.GENDER_KEY, user.gender or "Female")
        ageGroup = req_data.get(contracts.RecommendationContractRequest.AGE_GROUP_KEY, "")
        city = req_data.get(contracts.RecommendationContractRequest.CITY_KEY, user.city or "")

        from . import helper
        help = helper.RecommendationHelper()
        
        try:
            links = help.giveRecommendations(
                userid=userid,
                gender=gender,
                occasion=occasion,
                city=city,
                culture=culture,
                ageGroup=ageGroup,
                date=datetime.today().strftime("%Y-%m-%d"),
                time=datetime.now()
            )
        except Exception as e:
            return jsonify({
                "error": "Recommendation generation failed",
                "error_code": contracts.ErrorCodes.RECOMMENDATION_FAILED
            }), 500

        try:
            response = model.generate_content(
                f"""Generate 3 color palettes with 5 colors each for:
                Occasion: {occasion},
                Culture: {culture},
                Gender: {gender},
                Age: {ageGroup},
                City: {city}.
                Format: [[[hexColor,item], ...], ...]"""
            )
            color_palettes = parse_color_palette_response(response.text)
        except Exception as e:
            color_palettes = []
            print(f"Color palette generation failed: {e}")

        return jsonify({
            contracts.RecommendationContractResponse.LINKS: links,
            "COLOR_PALETTES": color_palettes
        }), 200

    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "error_code": contracts.ErrorCodes.SERVER_ERROR
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

        myfile = genai.upload_file(Path(temp_file_path))

        prompt = """Based on the uploaded image, can you suggest clothing items or outfit recommendations in JSON format?
            Include the following keys:

            - 'recommended_outfits': A list of outfit ideas with their names and descriptions.
            - 'accessories': Suggested matching accessories with their types and color schemes.
            - 'recommended_outfits': A list of outfit ideas with their names and descriptions in form [{'name':name, 'description':description}, ...].
            - 'style_tips': Any additional styling tips or details."""

        result = model.generate_content([myfile, prompt])
        response = result.text

        os.remove(temp_file_path)

        return jsonify({"recommendations": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500