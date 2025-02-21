from datetime import datetime
from functools import wraps
import logging
from django.http import JsonResponse
from django.shortcuts import redirect, render
from pymongo import MongoClient
from django.db import connection
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from trti_dashboard.settings import POWER_BI_EMBED_URL
from bson import ObjectId
from json import JSONEncoder

# Initialize logger
logger = logging.getLogger(__name__)

# Custom JSON Encoder for MongoDB ObjectId
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

# MongoDB Client Connection
client = MongoClient(
    '192.168.10.65',  
    username='Dashboard', 
    password='Pass@123',
    authSource='mpscSkillDevelopment',
    authMechanism='SCRAM-SHA-256'
)

# Function to Create User Session
def create_session(request, user_data):
    """Create a secure session for a logged-in user"""
    request.session.flush()
    request.session["user_id"] = user_data["id"]
    request.session["username"] = user_data["username"]
    request.session["is_authenticated"] = True
    request.session.set_expiry(3600)

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.GET.get("next", "dashboard")

        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            next_url = "dashboard"

        if username == "Admin" and password == "Admin":
            create_session(request, {"id": 1, "username": "Admin"})
            return redirect(next_url)

        messages.error(request, "Invalid username or password")
        return redirect("login")

    return render(request, "homepage/login.html")

# Logout View
def user_logout(request):
    if "username" in request.session:
        logger.info(f"User '{request.session.get('username')}' logged out.")
    
    request.session.flush()
    return redirect("login")

# Authentication Decorator
def check_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("is_authenticated"):
            logger.warning("Unauthorized access attempt - Redirecting to login")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

# Dashboard View
@check_auth
def dashboard(request):
    return render(request, "homepage/dashboard.html", {
        "username": request.session.get("username"),
        "powerbi_embed_url": POWER_BI_EMBED_URL,
        "last_updated": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    })

def get_database_data():
    """Helper function to fetch data from both databases"""
    try:
        # MySQL query
        mysql_query = """
            SELECT candidate_id, first_name, last_name, email_id, date_of_birth, 
                   maritalStatus, correspondence_state, correspondence_district, 
                   correspondence_taluka, correspondence_village, correspondence_pincode, caste
            FROM tbl_candidate 
            LIMIT 25
        """
        with connection.cursor() as cursor:
            cursor.execute(mysql_query)
            mysql_columns = [col[0] for col in cursor.description]
            mysql_data = cursor.fetchall()

        # MongoDB query
        db = client["mpscSkillDevelopment"]
        collection = db["tbl_candidate"]
        mongo_fields = {
            "_id": 1, "first_name": 1, "last_name": 1, "email_id": 1,
            "dateOfbirth": 1, "marital_status": 1, "com_state": 1,
            "com_district": 1, "com_taluka": 1, "com_village": 1,
            "pincode": 1, "caste": 1
        }
        mongo_docs = list(collection.find({}, mongo_fields).limit(25))
        mongo_columns = list(mongo_docs[0].keys()) if mongo_docs else []

        return {
            'mysql_columns': mysql_columns,
            'mysql_data': mysql_data,
            'mongo_columns': mongo_columns,
            'mongo_data': mongo_docs
        }
    except Exception as e:
        logger.error(f"Error fetching database data: {str(e)}")
        raise

# Extract Data View
@check_auth
def extract_view(request):
    """Main view for displaying extracted data"""
    try:
        data = get_database_data()
        return render(request, "homepage/extract.html", {
            "username": request.session.get("username"),
            "mysql_columns": data['mysql_columns'],
            "mysql_data": data['mysql_data'],
            "mongo_columns": data['mongo_columns'],
            "mongo_data": data['mongo_data'],
            "last_updated": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
    except Exception as e:
        logger.error(f"Error in extract view: {str(e)}")
        messages.error(request, "Error loading data. Please try again later.")
        return redirect("dashboard")

# New endpoint for AJAX updates
@check_auth
def get_updated_data(request):
    """API endpoint for fetching updated data"""
    try:
        data = get_database_data()
        
        # Convert MongoDB data to be JSON serializable
        mongo_data = []
        for doc in data['mongo_data']:
            converted_doc = {}
            for key, value in doc.items():
                if key == '_id':
                    converted_doc[key] = str(value)
                else:
                    converted_doc[key] = value
            mongo_data.append(converted_doc)

        return JsonResponse({
            'success': True,
            'data': {
                'mysql_data': [list(row) for row in data['mysql_data']],
                'mongo_data': mongo_data,
                'last_updated': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        })
    except Exception as e:
        logger.error(f"Error fetching updated data: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Failed to fetch updated data'
        }, status=500)

# Homepage View
def homepage(request):
    return render(request, "homepage/homepage.html", {
        "username": request.session.get("username")
    })

# Public Views
def index(request):
    return render(request, "homepage/index.html")

def contact_view(request):
    return render(request, "homepage/contact.html")

def about_view(request):
    return render(request, "homepage/about.html")

def session_timeout_view(request):
    return render(request, "homepage/session_timeout.html")

# Status Check View
def check_status(request):
    return JsonResponse({
        "status": "ok",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

# Authentication Status Check
def check_auth_status(request):
    return JsonResponse({
        "authenticated": request.session.get("is_authenticated", False),
        "username": request.session.get("username", None),
        "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
