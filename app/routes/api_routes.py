"""
REST API Endpoints for Dynamic AJAX updates (Live Order Status, Stock Toggle, Cart)
"""

from flask import Blueprint, jsonify, request, session
from app.db import get_collection, is_mongo_connected

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/system-status")
def system_status():
    """Returns database connection status."""
    return jsonify({
        "status": "healthy",
        "university": "Shobhit University Gangoh",
        "mongo_connected": is_mongo_connected(),
        "mode": "Live MongoDB" if is_mongo_connected() else "High-Fidelity Local Standalone Mode"
    })


@api_bp.route("/order-status/<token>")
def order_status_api(token):
    """Returns order state for live polling on student status page."""
    orders_col = get_collection("orders")
    order = orders_col.find_one({"token": token.upper()})

    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Sanitize _id for JSON serialization
    order_data = dict(order)
    if "_id" in order_data:
        order_data["_id"] = str(order_data["_id"])

    return jsonify({
        "token": order_data.get("token"),
        "status": order_data.get("status"),
        "total_amount": order_data.get("total_amount"),
        "created_at": order_data.get("created_at"),
        "estimated_mins": order_data.get("estimated_mins", 10),
        "items": order_data.get("items", [])
    })


@api_bp.route("/toggle-availability/<item_id>", methods=["POST"])
def toggle_availability_api(item_id):
    """Admin AJAX toggle for fast inventory stock management."""
    if session.get("user_role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    items_col = get_collection("menu_items")
    item = items_col.find_one({"item_id": item_id})

    if not item:
        return jsonify({"error": "Item not found"}), 404

    new_state = not item.get("is_available", True)
    items_col.update_one({"item_id": item_id}, {"$set": {"is_available": new_state}})

    return jsonify({
        "success": True,
        "item_id": item_id,
        "is_available": new_state,
        "status_label": "In Stock" if new_state else "Out of Stock"
    })

