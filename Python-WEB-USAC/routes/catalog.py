from flask import Blueprint, render_template, url_for, redirect, session
from models.products import loadProducts, saveProducts, getProductById

catalog_bp = Blueprint("catalog", __name__)

@catalog_bp.route("/catalog")
def products():
    if "cui" not in session:
        return redirect(url_for("auth.login"))
    
    products = loadProducts()
    print(products)
    return render_template("catalog.html", products=products)
