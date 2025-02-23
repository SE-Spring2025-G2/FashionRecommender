from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session
)

from flask_login import current_user, login_required

logosbp = Blueprint("logos", __name__)
@logosbp.route("/logos", methods=["GET"])
@login_required
# List of websites


def logos():
    
    website_name = ["shein.com",
    "boohoo.com",  
    "nike.com",
    "hm.com",
    "myntra.com",
    "mercari.com",
    "shop.app",
    "zalando.de",
    "uniqlo.com",
    "asos.com",
    "adidas.com",
    "farfetch.com",
    "macys.com",
    "net-a-porter.com",
    "zara.com",
    "urbanoutfitters.com",
    "matchesfashion.com",
    "ssense.com",
    "louisvuitton.com",
    "revolve.com",
    "gap.com",
    "zozo.jp",
    "puma.com",
    "levi.com",
    "bloomingdales.com",
    "depop.com",
    "llbean.com"]

    return render_template("logos.html",user=current_user, website_name=website_name, enumerate=enumerate)