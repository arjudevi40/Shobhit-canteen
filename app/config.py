import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "shobhit_univ_gangoh_fallback_secret_key_12345")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/shobhit_canteen")
    DB_NAME = os.getenv("DB_NAME", "shobhit_canteen")
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "127.0.0.1")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")

    # Fixed Sample Test Credentials loaded directly to guarantee seamless startup
    SAMPLE_CREDENTIALS = {
        "admin@shobhit.ac.in": {
            "name": "Prof. R. S. Chauhan",
            "role": "admin",
            "password": "admin123",
            "department": "Canteen & Campus Administration",
            "phone": "+91 98765 43210"
        },
        "student@shobhit.ac.in": {
            "name": "Aman Sharma",
            "role": "student",
            "password": "student123",
            "roll_no": "SUG2024CS042",
            "course": "B.Tech Computer Science (3rd Sem)",
            "phone": "+91 98980 12345"
        },
        "staff@shobhit.ac.in": {
            "name": "Dr. Priya Verma",
            "role": "student", # Treated as campus customer
            "password": "staff123",
            "roll_no": "FAC-EC-109",
            "course": "Faculty of Pharmacy & Health Sciences",
            "phone": "+91 97110 54321"
        }
    }

