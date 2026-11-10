"""
Student and Customer Routes for Shobhit University Gangoh Canteen System
Handles Home page, Food Menu browsing, Cart, Checkout simulation, and Order tracking.
"""

import random
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.db import get_collection, is_mongo_connected

student_bp = Blueprint("student", __name__)


def generate_token():
    """Generates an easy-to-read canteen token like SUG-1082"""
    num = random.randint(1001, 9999)
    return f"SUG-{num}"


@student_bp.route("/")
def index():
    """Home page with hero section, food categories, featured items, and university branding."""
    items_col = get_collection("menu_items")
    all_items = list(items_col.find())

    # Group sample featured items by category
    categories = ["Snacks", "Fast Food", "Meals", "Beverages"]
    categorized_items = {}
    for cat in categories:
        categorized_items[cat] = [item for item in all_items if item.get("category") == cat]

    # Overall featured picks
    featured_items = all_items[:6] if len(all_items) >= 6 else all_items

    return render_template(
        "index.html",
        categories=categories,
        categorized_items=categorized_items,
        featured_items=featured_items,
        is_mongo=is_mongo_connected()
    )


@student_bp.route("/menu")
def menu():
    """Complete food menu browsing with category filters and search."""
    items_col = get_collection("menu_items")
    selected_category = request.args.get("category", "All")
    search_query = request.args.get("q", "").strip().lower()

    filter_dict = {}
    if selected_category != "All":
        filter_dict["category"] = selected_category

    all_items = list(items_col.find(filter_dict))

    # Client-side / server-side search filter
    if search_query:
        all_items = [
            it for it in all_items
            if search_query in it.get("name", "").lower()
            or search_query in it.get("description", "").lower()
            or search_query in it.get("category", "").lower()
        ]

    categories = ["All", "Snacks", "Fast Food", "Meals", "Beverages"]

    return render_template(
        "menu.html",
        items=all_items,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        is_mongo=is_mongo_connected()
    )


@student_bp.route("/cart")
def cart():
    """Interactive cart overview and checkout configuration."""
    items_col = get_collection("menu_items")
    all_items = list(items_col.find())
    return render_template("cart.html", all_items=all_items)


@student_bp.route("/checkout", methods=["POST"])
def checkout():
    """Processes checkout simulation and creates an order token."""
    # Ensure student is identified, either via session or guest form input
    student_name = session.get("user_name") or request.form.get("name", "").strip() or "Guest Student"
    student_email = session.get("user_email") or request.form.get("email", "").strip() or "student@shobhit.ac.in"
    student_phone = session.get("phone") or request.form.get("phone", "").strip() or "+91 98765 00000"
    roll_no = session.get("roll_no") or request.form.get("roll_no", "").strip() or "SUG-2024"
    order_type = request.form.get("order_type", "Counter Pickup")
    delivery_spot = request.form.get("delivery_spot", "Canteen Counter 1")
    payment_method = request.form.get("payment_method", "Campus UPI")
    special_notes = request.form.get("special_notes", "").strip()

    # Parse ordered items JSON from client
    import json
    cart_items_raw = request.form.get("cart_data", "[]")
    try:
        cart_items = json.loads(cart_items_raw)
    except Exception:
        cart_items = []

    if not cart_items:
        flash("Your cart is empty! Please add some delicious snacks before checkout.", "warning")
        return redirect(url_for("student.menu"))

    # Compute total and verify availability
    items_col = get_collection("menu_items")
    processed_items = []
    total_amount = 0.0

    for item in cart_items:
        db_item = items_col.find_one({"item_id": item.get("item_id")})
        unit_price = float(db_item.get("price", 0)) if db_item else float(item.get("price", 0))
        qty = int(item.get("quantity", 1))
        subtotal = unit_price * qty
        total_amount += subtotal

        processed_items.append({
            "item_id": item.get("item_id"),
            "name": item.get("name") or (db_item.get("name") if db_item else "Item"),
            "price": unit_price,
            "quantity": qty,
            "subtotal": subtotal,
            "category": db_item.get("category", "General") if db_item else "General"
        })

    token = generate_token()
    now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    order_doc = {
        "token": token,
        "student_name": student_name,
        "student_email": student_email,
        "student_phone": student_phone,
        "roll_no": roll_no,
        "order_type": order_type,
        "delivery_spot": delivery_spot,
        "payment_method": payment_method,
        "special_notes": special_notes,
        "items": processed_items,
        "total_amount": round(total_amount, 2),
        "status": "Pending",  # Status pipeline: Pending -> Preparing -> Ready -> Delivered
        "created_at": now_str,
        "estimated_mins": 12
    }

    orders_col = get_collection("orders")
    orders_col.insert_one(order_doc)

    flash(f"Order #{token} placed successfully! Please collect your food when status is 'Ready'.", "success")
    return redirect(url_for("student.order_status", token=token))


@student_bp.route("/order-status/<token>")
def order_status(token):
    """Live order tracker showing status stepper and token details."""
    orders_col = get_collection("orders")
    order = orders_col.find_one({"token": token.upper()})

    if not order:
        flash(f"Order with Token #{token} not found.", "danger")
        return redirect(url_for("student.menu"))

    return render_template("order_status.html", order=order)


@student_bp.route("/my-orders")
def my_orders():
    """Displays order history for the currently logged in student or guest."""
    orders_col = get_collection("orders")
    user_email = session.get("user_email")

    if user_email:
        orders = list(orders_col.find({"student_email": user_email}))
    else:
        # Show recent orders
        orders = list(orders_col.find())[-10:]

    # Reverse so most recent is first
    orders.reverse()
    return render_template("my_orders.html", orders=orders)

