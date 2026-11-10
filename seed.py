#!/usr/bin/env python3
"""
Seed Script for Shobhit University Gangoh Canteen System
Loads sample food items, categories, and test user credentials into MongoDB.
Run this directly:
    python seed.py
"""

import sys
import os
import certifi
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

# Load configuration
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/shobhit_canteen")
DB_NAME = os.getenv("DB_NAME", "shobhit_canteen")

print("=" * 70)
print("  SHOBHIT UNIVERSITY GANGOH - CANTEEN SYSTEM SEED UTILITY")
print("=" * 70)
print(f"Connecting to MongoDB at: {MONGO_URI}")

# Pymongo connection with TLS options and certifi for Windows SSL compatibility
client_kwargs = {
    "serverSelectionTimeoutMS": 5000,
    "connectTimeoutMS": 5000,
    "socketTimeoutMS": 5000,
    "tlsAllowInvalidCertificates": True,
}
if "mongodb+srv://" in MONGO_URI or "tls=true" in MONGO_URI.lower() or "ssl=true" in MONGO_URI.lower():
    try:
        client_kwargs["tlsCAFile"] = certifi.where()
    except Exception:
        pass

try:
    client = MongoClient(MONGO_URI, **client_kwargs)
    client.admin.command("ping")
    db = client[DB_NAME]
    print("[SUCCESS] Connected to MongoDB database successfully!")
except Exception as e:
    print(f"[WARNING] Live MongoDB connection could not be established: {e}")
    print("[INFO] Fallback internal database will be automatically utilized when running wsgi.py.")
    print("=" * 70)
    sys.exit(0)

# Sample Users
users = [
    {
        "name": "Prof. R. S. Chauhan",
        "email": "admin@shobhit.ac.in",
        "password": "admin123",
        "role": "admin",
        "department": "Canteen & Campus Administration",
        "phone": "+91 98765 43210"
    },
    {
        "name": "Aman Sharma",
        "email": "student@shobhit.ac.in",
        "password": "student123",
        "role": "student",
        "department": "B.Tech Computer Science",
        "roll_no": "SUG2024CS042",
        "phone": "+91 98980 12345"
    },
    {
        "name": "Dr. Priya Verma",
        "email": "staff@shobhit.ac.in",
        "password": "staff123",
        "role": "student",
        "department": "Faculty of Pharmacy & Health Sciences",
        "roll_no": "FAC-PH-202",
        "phone": "+91 97110 54321"
    }
]

# Sample Canteen Menu Items
menu_items = [
    # Snacks
    {
        "item_id": "SNK01",
        "name": "Hot Crispy Samosa (2 Pcs)",
        "category": "Snacks",
        "price": 25.0,
        "description": "Crispy golden crust filled with spiced potatoes, peas, served with sweet tamarind and spicy mint chutney.",
        "veg": True,
        "is_available": True,
        "prep_time": "5 mins",
        "calories": "280 kcal",
        "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "SNK02",
        "name": "Khasta Aloo Kachori (2 Pcs)",
        "category": "Snacks",
        "price": 30.0,
        "description": "Flaky, deep-fried pastry stuffed with spiced lentil/potato filling, served with Saharanpur-style tangy aloo sabzi.",
        "veg": True,
        "is_available": True,
        "prep_time": "5 mins",
        "calories": "310 kcal",
        "image": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "SNK03",
        "name": "Paneer Bread Pakora",
        "category": "Snacks",
        "price": 35.0,
        "description": "Double bread slice stuffed with soft cottage cheese & mint chutney, coated in spiced chickpea batter.",
        "veg": True,
        "is_available": True,
        "prep_time": "8 mins",
        "calories": "340 kcal",
        "image": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "SNK04",
        "name": "Crispy Veg Cutlet (2 Pcs)",
        "category": "Snacks",
        "price": 30.0,
        "description": "Golden crumb-fried vegetable patties with beetroot, carrots, potatoes, and mild Indian spices.",
        "veg": True,
        "is_available": True,
        "prep_time": "10 mins",
        "calories": "220 kcal",
        "image": "https://images.unsplash.com/photo-1541832676-9b763b0239ab?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "SNK05",
        "name": "Spicy Aloo Patty",
        "category": "Snacks",
        "price": 20.0,
        "description": "Crisp multi-layered puff pastry filled with tempered cumin potato mash.",
        "veg": True,
        "is_available": True,
        "prep_time": "3 mins",
        "calories": "260 kcal",
        "image": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=500&auto=format&fit=crop&q=80"
    },

    # Fast Food
    {
        "item_id": "FF01",
        "name": "SU-Gangoh Special Veg Burger",
        "category": "Fast Food",
        "price": 50.0,
        "description": "Toasted sesame bun with a crispy herb potato patty, fresh tomato, crisp lettuce, onion rings, and tandoori mayo.",
        "veg": True,
        "is_available": True,
        "prep_time": "10 mins",
        "calories": "390 kcal",
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "FF02",
        "name": "Double Cheese Margherita Burger",
        "category": "Fast Food",
        "price": 70.0,
        "description": "Melted cheese slice over a golden vegetable cutlet, seasoned with oregano and creamy garlic sauce.",
        "veg": True,
        "is_available": True,
        "prep_time": "12 mins",
        "calories": "460 kcal",
        "image": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "FF03",
        "name": "Desi Masala Veg Chowmein",
        "category": "Fast Food",
        "price": 60.0,
        "description": "Wok-tossed noodles with shredded cabbage, bell peppers, carrots, spring onions, soy and chili sauce.",
        "veg": True,
        "is_available": True,
        "prep_time": "10 mins",
        "calories": "380 kcal",
        "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "FF04",
        "name": "Bombay Grilled Veg Sandwich",
        "category": "Fast Food",
        "price": 55.0,
        "description": "Jumbo toasted sandwich with layers of cucumber, tomato, potato, green chutney, and chat masala butter.",
        "veg": True,
        "is_available": True,
        "prep_time": "8 mins",
        "calories": "310 kcal",
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "FF05",
        "name": "Crispy French Fries (Peri-Peri)",
        "category": "Fast Food",
        "price": 45.0,
        "description": "Crisp potato fries dusted with hot and tangy African peri-peri seasoning.",
        "veg": True,
        "is_available": True,
        "prep_time": "7 mins",
        "calories": "290 kcal",
        "image": "https://images.unsplash.com/photo-1576107232684-1279f3908594?w=500&auto=format&fit=crop&q=80"
    },

    # Meals
    {
        "item_id": "MEL01",
        "name": "Special Shobhit Thali",
        "category": "Meals",
        "price": 110.0,
        "description": "Wholesome student thali with Dal Makhani, Shahi Paneer, Jeera Rice, 4 Butter Roti, Fresh Salad, and Sweet.",
        "veg": True,
        "is_available": True,
        "prep_time": "12 mins",
        "calories": "780 kcal",
        "image": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "MEL02",
        "name": "Punjabi Chole Bhature (2 Bhature)",
        "category": "Meals",
        "price": 80.0,
        "description": "Fluffy balloon bhature served with rich dark spiced Amritsari chole, pickled onions, and green chilies.",
        "veg": True,
        "is_available": True,
        "prep_time": "10 mins",
        "calories": "650 kcal",
        "image": "https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "MEL03",
        "name": "Homestyle Rajma Chawal Bowl",
        "category": "Meals",
        "price": 70.0,
        "description": "Slow-cooked Kashmiri kidney beans simmered in tomato gravy served over fragrant basmati rice.",
        "veg": True,
        "is_available": True,
        "prep_time": "7 mins",
        "calories": "520 kcal",
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "MEL04",
        "name": "Kadhi Pakora with Steamed Rice",
        "category": "Meals",
        "price": 65.0,
        "description": "Tangy gram flour curd kadhi with soft onion fritters and aromatic jeera tadka.",
        "veg": True,
        "is_available": True,
        "prep_time": "7 mins",
        "calories": "480 kcal",
        "image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500&auto=format&fit=crop&q=80"
    },

    # Beverages
    {
        "item_id": "BEV01",
        "name": "Kulhad Masala Chai",
        "category": "Beverages",
        "price": 15.0,
        "description": "Traditional clay cup tea infused with crushed ginger, green cardamom, cloves, and holy basil.",
        "veg": True,
        "is_available": True,
        "prep_time": "3 mins",
        "calories": "85 kcal",
        "image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "BEV02",
        "name": "Special Hot Filter Coffee",
        "category": "Beverages",
        "price": 25.0,
        "description": "Freshly brewed aromatic South Indian chicory blend coffee with frothy steamed milk.",
        "veg": True,
        "is_available": True,
        "prep_time": "5 mins",
        "calories": "110 kcal",
        "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "BEV03",
        "name": "Thick Chilled Cold Coffee",
        "category": "Beverages",
        "price": 45.0,
        "description": "Creamy blended cold coffee with chocolate drizzle and vanilla ice cream scoop.",
        "veg": True,
        "is_available": True,
        "prep_time": "5 mins",
        "calories": "260 kcal",
        "image": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "BEV04",
        "name": "Creamy Sweet Punjabi Lassi",
        "category": "Beverages",
        "price": 35.0,
        "description": "Rich churned yogurt drink topped with a layer of fresh malai and crushed pistachios.",
        "veg": True,
        "is_available": True,
        "prep_time": "4 mins",
        "calories": "240 kcal",
        "image": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&auto=format&fit=crop&q=80"
    },
    {
        "item_id": "BEV05",
        "name": "Warm Gulab Jamun (2 Pcs)",
        "category": "Beverages",
        "price": 30.0,
        "description": "Soft khoya dumplings dipped in saffron rose scented sugar syrup.",
        "veg": True,
        "is_available": True,
        "prep_time": "2 mins",
        "calories": "290 kcal",
        "image": "https://images.unsplash.com/photo-1593701461250-d7b22dfd3a77?w=500&auto=format&fit=crop&q=80"
    }
]

# Reset and insert users
db.users.delete_many({})
db.users.insert_many(users)
print(f"[OK] Seeded {len(users)} test users successfully.")

# Reset and insert menu items
db.menu_items.delete_many({})
db.menu_items.insert_many(menu_items)
print(f"[OK] Seeded {len(menu_items)} delicious canteen menu items successfully.")

print("\n--- SAMPLE TEST LOGIN CREDENTIALS ---")
print("1. Admin / Canteen In-charge:")
print("   Email:    admin@shobhit.ac.in")
print("   Password: admin123")
print("\n2. Student:")
print("   Email:    student@shobhit.ac.in")
print("   Password: student123")
print("\n3. Staff / Faculty:")
print("   Email:    staff@shobhit.ac.in")
print("   Password: staff123")
print("=" * 70)
print("Seed process completed successfully!")

