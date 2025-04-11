from flask import Blueprint, flash, render_template, url_for, redirect, session,jsonify
from models.products import loadProducts

cart_bp = Blueprint("cart", __name__)

def getCart():
    #Obtiene el lcarrito o crea uno nuevo
    return session.get("cart",{})

def saveCart(cart):
    # Guarda el carrito en la session
    session["cart"] = cart
    session.modified = True

@cart_bp.route("/add/<int:productId>", methods=["POST"])
def addToCart(productId):
    cart = getCart()
    products = loadProducts()

    product = next((p for p in products if p["id"]== productId), None)
    if not product:
        return jsonify({"error": "producto no encontrado"}), 404 #codigo 404 es decir que no ha encontrado el objeto
    
    # cart: ("productId" : 1, "cantidad": 2)

    if str(productId) in (cart):
        #añadimos producto repetido
        cart[str(productId)]["quantity"] += 1
    else:
        # añadimos producto por primera vez
        cart[str(productId)] = {
            "name": product["name"],
            "price": product["price"],
            "quantity": 1,
            "picture": product["picture"]
        }
    saveCart(cart)
    return redirect(url_for("catalog.products"))

def getCartCount():
    cart = getCart()
    # item["quantity"] for item in cart.values()
    # 1. recorremos los avlores del cart
    # 2. se reccoren con la variable item
    # 3. necesitamos el atributo quantity de item para obtener los valores

    '''
        acum = 0
        for item in cart.values()
            acum += item[quantity]
            return acum
    '''

    return sum(item["quantity"] for item in cart.values())

# ver nuestro carrito de compras
@cart_bp.route("/cart")
def viewCart():
    cart = getCart()
    total = sum(item["price"] for item in cart.values())
    cartCount = getCartCount()
    return render_template("cart.html", cart=cart, total=total, cartCount=cartCount)

@cart_bp.route("/remove/<int:productId>", methods=["POST"])
def removeFromCart(productId):
    cart = getCart()

    if str(productId) in (cart):
        del cart[str(productId)]
        saveCart(cart)
        return redirect(url_for("cart.viewCart"))

@cart_bp.route("/removequantity/<int:productId>", methods=["POST"])
def removeXQuantityFromCart(productId):
    cart = getCart()

    if str(productId) in (cart):

        cart[str(productId)]["quantity"] -= 1

        '''
        for newCart in cart:
            if newCart[str(productId)] == cart[str(productId)]:
                int(newCart["quantity"]) -= 1
                cart = newCart
            if newCart["quantity"] == 0:
                del newCart[str(productId)]
                cart = newCart
        '''
    if cart[str(productId)]["quantity"] == 0:
        del cart[str(productId)]

    saveCart(cart)
    return redirect(url_for("cart.viewCart"))

@cart_bp.route("/delete", methods=["POST"])
def deleteCart():
    

    paidCart = getCart()
    paidCart.clear()

    #if paidCart == None:
    #    flash("Pago cancelado", "danger")
    #else:
    flash("Pago exitoso", "success")

    saveCart(paidCart)
    return redirect(url_for("cart.viewCart"))
