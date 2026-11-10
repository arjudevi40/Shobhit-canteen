"""
Administrator & Canteen Manager Routes for Shobhit University Gangoh
Manages live orders, kitchen queues, daily menu items, and stock availability.
"""

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.db import get_collection, is_mongo_connected

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_email" not in session or session.get("user_role") != "admin":
            flash("Admin privilege required. Please login with Canteen Admin credentials.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """Live Kitchen & Canteen Admin Dashboard."""
    orders_col = get_collection("orders")
    items_col = get_collection("menu_items")

    status_filter = request.args.get("status", "All")
    query = {}
    if status_filter != "All":
        query["status"] = status_filter

    orders = list(orders_col.find(query))
    orders.reverse()

    all_orders = list(orders_col.find())
    total_orders = len(all_orders)
    pending_count = len([o for o in all_orders if o.get("status") in ("Pending", "Preparing")])
    ready_count = len([o for o in all_orders if o.get("status") == "Ready"])
    delivered_count = len([o for o in all_orders if o.get("status") == "Delivered"])
    total_revenue = sum(o.get("total_amount", 0) for o in all_orders if o.get("status") != "Cancelled")

    in_stock_items = items_col.count_documents({"is_available": True})
    total_items = items_col.count_documents({})

    return render_template(
        "admin/dashboard.html",
        orders=orders,
        status_filter=status_filter,
        total_orders=total_orders,
        pending_count=pending_count,
        ready_count=ready_count,
        delivered_count=delivered_count,
        total_revenue=round(total_revenue, 2),
        in_stock_items=in_stock_items,
        total_items=total_items,
        is_mongo=is_mongo_connected()
    )


@admin_bp.route("/orders/update-status", methods=["POST"])
@admin_required
def update_order_status():
    """Updates the preparation / delivery state of an order."""
    token = request.form.get("token", "").strip().upper()
    new_status = request.form.get("status", "").strip()

    valid_statuses = ["Pending", "Preparing", "Ready", "Delivered", "Cancelled"]
    if new_status not in valid_statuses:
        flash("Invalid status selected.", "danger")
        return redirect(url_for("admin.dashboard"))

    orders_col = get_collection("orders")
    res = orders_col.update_one({"token": token}, {"$set": {"status": new_status}})

    if res.matched_count > 0:
        flash(f"Order #{token} status updated to '{new_status}' successfully.", "success")
    else:
        flash(f"Order #{token} not found.", "danger")

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/menu")
@admin_required
def menu_management():
    """Menu & inventory management view to add, edit, or toggle items."""
    items_col = get_collection("menu_items")
    category_filter = request.args.get("category", "All")

    query = {}
    if category_filter != "All":
        query["category"] = category_filter

    items = list(items_col.find(query))
    categories = ["Snacks", "Fast Food", "Meals", "Beverages"]

    return render_template(
        "admin/menu_mgmt.html",
        items=items,
        categories=categories,
        category_filter=category_filter,
        is_mongo=is_mongo_connected()
    )


@admin_bp.route("/menu/toggle-stock/<item_id>", methods=["POST"])
@admin_required
def toggle_stock(item_id):
    """Toggles item availability between In Stock and Out of Stock."""
    items_col = get_collection("menu_items")
    item = items_col.find_one({"item_id": item_id})

    if item:
        new_state = not item.get("is_available", True)
        items_col.update_one({"item_id": item_id}, {"$set": {"is_available": new_state}})
        status_text = "In Stock" if new_state else "Out of Stock"
        flash(f"'{item.get('name')}' marked as {status_text}.", "success")
    else:
        flash(f"Item {item_id} not found.", "danger")

    return redirect(request.referrer or url_for("admin.menu_management"))


@admin_bp.route("/menu/add", methods=["POST"])
@admin_required
def add_menu_item():
    """Adds a new delicious food item to the university canteen menu."""
    items_col = get_collection("menu_items")

    name = request.form.get("name", "").strip()
    category = request.form.get("category", "Snacks").strip()
    price_raw = request.form.get("price", "0").strip()
    description = request.form.get("description", "").strip()
    image = request.form.get("image", "").strip()
    prep_time = request.form.get("prep_time", "10 mins").strip()
    veg = request.form.get("veg") == "true" or request.form.get("veg") == "on"

    if not name or not price_raw:
        flash("Food item name and price are required.", "danger")
        return redirect(url_for("admin.menu_management"))

    try:
        price = float(price_raw)
    except ValueError:
        flash("Invalid price value.", "danger")
        return redirect(url_for("admin.menu_management"))

    # Generate an item code
    import random
    prefix = category[:3].upper()
    item_id = f"{prefix}{random.randint(10, 99)}"

    # Default fallback food images by category if none provided
    if not image:
        fallbacks = {
            "Snacks": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&auto=format&fit=crop&q=80",
            "Fast Food": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=80",
            "Meals": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=500&auto=format&fit=crop&q=80",
            "Beverages": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500&auto=format&fit=crop&q=80"
        }
        image = fallbacks.get(category, fallbacks["Snacks"])

    new_item = {
        "item_id": item_id,
        "name": name,
        "category": category,
        "price": price,
        "description": description or f"Freshly prepared {name} made with quality ingredients.",
        "veg": veg,
        "is_available": True,
        "prep_time": prep_time,
        "calories": "250 kcal",
        "image": image
    }

    items_col.insert_one(new_item)
    flash(f"New item '{name}' added to {category} successfully!", "success")
    return redirect(url_for("admin.menu_management"))


@admin_bp.route("/menu/delete/<item_id>", methods=["POST"])
@admin_required
def delete_menu_item(item_id):
    """Deletes an item from the canteen menu."""
    items_col = get_collection("menu_items")
    res = items_col.delete_one({"item_id": item_id})
    if res.deleted_count > 0:
        flash("Item removed from canteen menu.", "info")
    else:
        flash("Item could not be found.", "danger")
    return redirect(url_for("admin.menu_management"))

