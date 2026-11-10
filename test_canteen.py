"""
Automated Verification Suite for Shobhit University Gangoh Canteen System
Tests routes, authentication, cart checkout, token generation, admin operations, and APIs.
"""

import json
import unittest
from app import create_app
from app.db import get_collection


class TestShobhitCanteen(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

    def test_01_home_page(self):
        """Test home page displays university branding and categories."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn("Shobhit University", html)
        self.assertIn("Snacks", html)
        self.assertIn("Fast Food", html)
        self.assertIn("Meals", html)
        self.assertIn("Beverages", html)
        print("[PASS] Test 1: Home page loads with university branding and categories.")

    def test_02_menu_page_and_filtering(self):
        """Test menu page and category filters."""
        res = self.client.get("/menu")
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn("Samosa", html)
        self.assertIn("Burger", html)
        self.assertIn("Thali", html)

        # Test category filter
        res_snacks = self.client.get("/menu?category=Snacks")
        self.assertEqual(res_snacks.status_code, 200)
        html_snacks = res_snacks.data.decode("utf-8")
        self.assertIn("Samosa", html_snacks)
        print("[PASS] Test 2: Menu page & category filtering functioning correctly.")

    def test_03_login_authentication(self):
        """Test student and admin authentication with fixed test credentials."""
        # 1. Student login
        res_stu = self.client.post("/login", data={
            "email": "student@shobhit.ac.in",
            "password": "student123"
        }, follow_redirects=True)
        self.assertEqual(res_stu.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("user_role"), "student")
            self.assertEqual(sess.get("user_email"), "student@shobhit.ac.in")

        # 2. Logout
        self.client.get("/logout")
        with self.client.session_transaction() as sess:
            self.assertNotIn("user_email", sess)

        # 3. Admin login
        res_adm = self.client.post("/login", data={
            "email": "admin@shobhit.ac.in",
            "password": "admin123"
        }, follow_redirects=True)
        self.assertEqual(res_adm.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("user_role"), "admin")
        print("[PASS] Test 3: Fixed credentials login & role assignment verified.")

    def test_04_cart_and_checkout_simulation(self):
        """Test placing an order, generating token, and live order tracking."""
        sample_cart = [
            {"item_id": "SNK01", "name": "Hot Crispy Samosa (2 Pcs)", "price": 25.0, "quantity": 2},
            {"item_id": "BEV01", "name": "Kulhad Masala Chai", "price": 15.0, "quantity": 1}
        ]

        res = self.client.post("/checkout", data={
            "name": "Aman Sharma",
            "roll_no": "SUG2024CS042",
            "phone": "+91 98980 12345",
            "delivery_spot": "Counter 1 (Main Hall)",
            "payment_method": "Campus UPI",
            "special_notes": "Extra crispy samosa please",
            "cart_data": json.dumps(sample_cart)
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn("SUG-", html)
        self.assertIn("Official Canteen Order Token", html)
        self.assertIn("Order Information", html)

        # Extract token from the page
        import re
        match = re.search(r"SUG-\d{4}", html)
        self.assertIsNotNone(match)
        token = match.group(0)

        # Verify API status endpoint
        res_api = self.client.get(f"/api/order-status/{token}")
        self.assertEqual(res_api.status_code, 200)
        api_data = json.loads(res_api.data.decode("utf-8"))
        self.assertEqual(api_data["token"], token)
        self.assertEqual(api_data["status"], "Pending")
        self.assertEqual(api_data["total_amount"], 65.0)
        print(f"[PASS] Test 4: Checkout simulation created order token: {token} with total: INR {api_data['total_amount']}.")

    def test_05_admin_dashboard_and_order_update(self):
        """Test admin dashboard access, status changes, and stock toggle."""
        # Log in as admin
        self.client.post("/login", data={
            "email": "admin@shobhit.ac.in",
            "password": "admin123"
        }, follow_redirects=True)

        # View dashboard
        res_dash = self.client.get("/admin/dashboard")
        self.assertEqual(res_dash.status_code, 200)
        html_dash = res_dash.data.decode("utf-8")
        self.assertIn("Campus Kitchen & Order Operations", html_dash)

        # Create a test order to update
        orders_col = get_collection("orders")
        test_token = "SUG-9999"
        orders_col.insert_one({
            "token": test_token,
            "student_name": "Test Student",
            "roll_no": "SUG-TEST-01",
            "items": [{"name": "Burger", "price": 50.0, "quantity": 1}],
            "total_amount": 50.0,
            "status": "Pending",
            "delivery_spot": "Counter 1",
            "payment_method": "Campus UPI",
            "created_at": "2026-10-31 18:30 PM"
        })

        # Update order status to "Preparing"
        res_upd = self.client.post("/admin/orders/update-status", data={
            "token": test_token,
            "status": "Preparing"
        }, follow_redirects=True)
        self.assertEqual(res_upd.status_code, 200)

        # Verify in DB
        updated_order = orders_col.find_one({"token": test_token})
        self.assertEqual(updated_order["status"], "Preparing")

        # Test stock toggle API
        res_toggle = self.client.post("/api/toggle-availability/SNK01")
        self.assertEqual(res_toggle.status_code, 200)
        data = json.loads(res_toggle.data.decode("utf-8"))
        self.assertTrue(data["success"])
        print("[PASS] Test 5: Admin dashboard, status update, and stock toggle API verified.")


if __name__ == "__main__":
    unittest.main()
