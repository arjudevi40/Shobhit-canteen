# Shobhit University Gangoh - Canteen Management System

An intuitive, lightweight, and modern University Canteen Management System built specifically for **Shobhit University Gangoh** (Saharanpur, Uttar Pradesh).

The platform allows students, faculty, and campus staff to browse categories, order food, make digital payments, and receive live pickup tokens to eliminate long lunchtime queues. A dedicated Kitchen Admin Dashboard empowers canteen staff to view active orders in real time, advance queue states, and toggle menu availability with instant switches.

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, Vanilla CSS3 (custom responsive design with university branding & modern variables), JavaScript (Fetch API, Cart state, Live polling).
- **Backend:** Python Flask 3.x (Modular Application Factory pattern with Blueprints).
- **Database:** MongoDB via PyMongo (with automated zero-dependency fallback store for seamless startup anywhere).
- **Configuration:** Python-dotenv for environment variables.

---

## 📂 Project Structure

```text
SHOBHIT Canteen/
├── .env                     # Local environment settings
├── .env.example             # Template environment configuration
├── requirements.txt         # Python library dependencies
├── seed.py                  # Standalone database seeding utility
├── wsgi.py                  # Main WSGI application entry point
├── app/
│   ├── __init__.py          # Flask application factory & filters
│   ├── config.py            # Central configuration & fixed test credentials
│   ├── db.py                # Ultra-reliable MongoDB connection with SSL/TLS bypass
│   ├── routes/
│   │   ├── __init__.py      # Blueprints exporter
│   │   ├── auth_routes.py   # Student & Admin authentication, logout, demo logins
│   │   ├── student_routes.py# Home, Menu, Cart, Checkout, Token status, My Orders
│   │   ├── admin_routes.py  # Kitchen display, Order status updates, Menu & Stock CRUD
│   │   └── api_routes.py    # REST APIs for live order polling & stock toggle switches
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css    # Clean, modern, responsive CSS
│   │   │   └── admin.css    # Kitchen display and admin table styles
│   │   └── js/
│   │       ├── main.js      # Cart management, live search, toast notifications
│   │       └── admin.js     # Stock toggling and modal interactions
│   └── templates/
│       ├── base.html        # Main institutional layout with navbar & footer
│       ├── index.html       # Clean home dashboard with hero & category highlights
│       ├── login.html       # Unified student & admin login with 1-click test fill
│       ├── menu.html        # Categorized food menu with live search & filters
│       ├── cart.html        # Cart review, pickup options & checkout simulation
│       ├── order_status.html# Live visual order progress stepper & token display
│       ├── my_orders.html   # Past dining order history
│       └── admin/
│           ├── dashboard.html # Live kitchen order management & metric cards
│           └── menu_mgmt.html # Real-time stock toggle & food item creator
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- (Optional) MongoDB installed locally or a free MongoDB Atlas connection string.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Database (.env)
Edit `.env` to configure your MongoDB connection:
```ini
SECRET_KEY=shobhit_university_gangoh_canteen_secret_key_2026_secure!
MONGO_URI=mongodb://localhost:27017/shobhit_canteen
DB_NAME=shobhit_canteen
PORT=5000
HOST=127.0.0.1
FLASK_DEBUG=True
```

### 4. Seed Food Items & Test Users
Run the seeder script to populate default canteen dishes:
```bash
python seed.py
```

### 5. Start the Server
Launch the application:
```bash
python wsgi.py
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:5000/`**

---

## 🔐 Fixed Sample Test Credentials

To ensure complete reliability and zero startup dependency issues, the application includes pre-configured sample credentials:

| Role | Email ID | Password | Description |
|---|---|---|---|
| **Canteen Admin** | `admin@shobhit.ac.in` | `admin123` | Full access to Kitchen Display System & Stock Manager |
| **Student** | `student@shobhit.ac.in` | `student123` | Aman Sharma (Roll No: SUG2024CS042) |
| **Faculty / Staff** | `staff@shobhit.ac.in` | `staff123` | Dr. Priya Verma (Faculty of Pharmacy) |

*Tip: On the `/login` page, you can simply click the **"🎓 Student Demo"** or **"🛡️ Admin Demo"** buttons to autofill these credentials immediately.*

---

## 🛡️ Reliable Database Connection (`app/db.py`)

To completely prevent Windows TLS/SSL certificate handshake issues commonly encountered with MongoDB Atlas or local socket permission constraints:
- PyMongo client is configured with `tlsAllowInvalidCertificates=True` and `serverSelectionTimeoutMS=4000`.
- Includes `tlsCAFile=certifi.where()` for robust SSL CA validation.
- **Fail-Safe Mechanism:** If a live MongoDB instance is offline, the app seamlessly falls back to a high-fidelity in-memory database store with the exact same PyMongo query interface (`find`, `insert_one`, `update_one`, `delete_one`, etc.). The app will **never crash on startup**.

---

## 🍱 Canteen Features

### 1. Home Page (`/`)
- University branding: *Shobhit University Gangoh Canteen Express*.
- Live Canteen opening status (8:30 AM – 8:30 PM).
- Category tiles: **Snacks** (Samosa, Kachori), **Fast Food** (Burgers, Chowmein), **Meals** (North Indian Thali, Rajma Chawal), and **Beverages** (Kulhad Chai, Lassi).
- Popular campus highlights with quick "+ Add to Cart" buttons.

### 2. Student Panel (`/menu`, `/cart`, `/order-status/<token>`)
- Category tabs and instant live search (no page reload).
- Pure veg indicators with green badge.
- Interactive cart counter with item increments and price totals.
- Checkout simulation with pickup spot selection (Counter 1, Counter 2, Library Lawn) and simulated payment options (Campus UPI, Counter Cash, Student ID Wallet).
- **Instant Token Generation** (e.g. `SUG-1048`).
- **Live Order Tracker:** Visual 4-step progress stepper (*Order Placed* → *In Kitchen* → *Ready for Pickup* → *Collected*) that auto-polls the server every 4 seconds.

### 3. Kitchen Admin Dashboard (`/admin/dashboard`, `/admin/menu`)
- Overview metrics: Today's Orders, Kitchen Queue, Ready Orders, Total Revenue.
- Live Kitchen Display Table with one-click status transitions.
- Menu & Stock Management:
  - Real-time stock toggle switch (*In Stock* / *Out of Stock*).
  - Add New Food Item modal dialog.
  - Delete or modify items.

