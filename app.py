from flask import Flask, render_template, redirect, url_for, session, flash, request, g
import requests
import sqlite3
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'our_secret_key'
DATABASE = 'data.db'

API_KEY = ""

# Functions for fetching data
def get_hiking_park():
    url = "https://developer.nps.gov/api/v1/activities/parks"
    params = {
        "api_key": API_KEY,
        "id": "BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data and data["data"]:
        parks = data["data"][0]["parks"]
        return [
            {
                "Park Name": park.get("fullName"),
                "State": park.get("states"),
                "Designation": park.get("designation")
            }
            for park in parks
        ]
    else:
        return []

def get_park_info():
    url = "https://developer.nps.gov/api/v1/parks"
    params = {
        "api_key": API_KEY,
        "limit": 50,  # Maximum items per page
        "start": 0    # Start from the first item
    }
    all_parks = []
    
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        if "data" in data and data["data"]:
            parks = [
                {
                    "Park Name": park.get("fullName"),
                    "Park Image": park.get("images", []),
                    "Description": park.get("description"),
                    "Directions": park.get("directionsInfo"),
                    "State": park.get("states"),
                    "City and State": list(
                        {
                            (address.get("city"), address.get("stateCode"))
                            for address in park.get("addresses", [])
                        }
                    ),
                    "Activities": [
                        activity.get("name") for activity in park.get("activities", [])
                    ]
                }
                for park in data["data"]
            ]
            all_parks.extend(parks)
            
            # Increment the start parameter to get the next page
            params["start"] += params["limit"]
        else:
            # Break the loop if no more data is returned
            break
    
    return all_parks

def get_campgrounds():
    url = "https://developer.nps.gov/api/v1/campgrounds"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data and data["data"]:
        return [
            {
                "Accessibility": campground.get("accessibility", {}).get("accessRoads", []),
                "Amenities": campground.get("amenities", {}),
                "Campsites": campground.get("campsites", {}),
                "Contacts": campground.get("contacts", {}),
                "Description": campground.get("description")
            }
            for campground in data["data"]
        ]
    else:
        return []

def get_alerts():
    url = "https://developer.nps.gov/api/v1/alerts"
    params = {
        "api_key": API_KEY,
        "category": "Park Closure"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data and data["data"]:
        return [
            {
                "Title": alert.get("title"),
                "Description": alert.get("description"),
                "Park Code": alert.get("parkCode")
            }
            for alert in data["data"]
        ]
    else:
        return []

def get_things_to_do():
    url = "https://developer.nps.gov/api/v1/thingstodo"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data and data["data"]:
        return [
            {
                "Accessibility": activity.get("accessibility", {}),
                "Activities": [act.get("name") for act in activity.get("activities", [])],
                "Description": activity.get("description"),
                "Amenities": activity.get("amenities", {}),
                "Are Pets Permitted": activity.get("arePetsPermitted"),
                "Fees": activity.get("fees", []),
                "Time Of Day": activity.get("timeOfDay", []),
                "Topics": [topic.get("name") for topic in activity.get("topics", [])]
            }
            for activity in data["data"]
        ]
    else:
        return []

def get_visitor_centers():
    url = "https://developer.nps.gov/api/v1/visitorcenters"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data and data["data"]:
        return [
            {
                "Contacts": {
                    "Email Address": [
                        email.get("emailAddress") for email in center.get("contacts", {}).get("emailAddresses", [])
                    ],
                    "Phone Numbers": [
                        phone.get("phoneNumber") for phone in center.get("contacts", {}).get("phoneNumbers", [])
                    ]
                },
                "Description": center.get("description"),
                "Title": center.get("name"),
                "Park Code": center.get("parkCode"),
                "Direction Info": center.get("directionsInfo"),
                "Operating Hours": [
                    {
                        "Standard Hours": hours.get("standardHours", {}),
                        "Description": hours.get("description")
                    }
                    for hours in center.get("operatingHours", [])
                ]
            }
            for center in data["data"]
        ]
    else:
        return []
    
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db
           
# Routes
@app.route('/')
def home():
    message = "Welcome to our Final Project!"
    return render_template('home.html', message=message)

@app.route('/hiking-parks')
def hiking_parks():
    parks = get_hiking_park()
    return render_template('hiking_parks.html', parks=parks)

@app.route('/park-info')
def park_info():

    park_info = get_park_info()
    return render_template('parks.html', park_info=park_info)

@app.route('/campgrounds')
def campgrounds():

    campgrounds = get_campgrounds()
    return render_template('campgrounds.html', campgrounds=campgrounds)

@app.route('/park-alerts')
def park_alerts():
    alerts = get_alerts()
    return render_template('park_alerts.html', alerts=alerts)

@app.route('/things-to-do')
def things_to_do():
    things_to_do = get_things_to_do()
    return render_template('activites.html', things_to_do=things_to_do)

@app.route('/visitor-centers')
def visitor_centers():
    visitor_centers = get_visitor_centers()
    return render_template('visitor_centers.html', visitor_centers=visitor_centers)

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username exists and password is correct
        db = get_db()  # Get database connection
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and user[2] == password:  # Compare password (assuming it's stored in the 3rd column)
            flash("Welcome back, {}!".format(username), 'success')
            session['logged_in'] = True  # Store the logged-in state in the session
            session['username'] = username
            return redirect(url_for('account'))  # Redirect to the account page
        else:
            flash("Invalid credentials. Try again.", 'error')
            return render_template('login.html')  # Stay on the login page

    return render_template('login.html')


@app.route('/account')
def account():
    # Check if the user is logged in
    if not session.get('logged_in'):
        flash("Please log in to access your account.", 'error')
        return redirect(url_for('log_in'))  # Redirect if not logged in

    # Retrieve user data if logged in
    username = session.get('username', 'Guest')  # Default to 'Guest' if username not in session
    # Optional: Fetch saved items (if using a database)
    saved_items = []  # Replace with database fetch if needed
    return render_template('account.html', username=username, saved_items=saved_items)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session (logs out the user)
    flash("You have successfully logged out.", "success")
    return redirect(url_for('home'))  # Redirect to the home page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            db = get_db()  # Get database connection
            cursor = db.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Username already exists. Please choose a different one.", 'error')
                return render_template('register.html')

            # Insert the new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()

            flash("Account created successfully!", 'success')
            session['logged_in'] = True  # Store the logged-in state in the session
            session['username'] = username
            return redirect(url_for('home'))  # Redirect to the home page
        else:
            flash("Please fill in all fields.", 'error')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/save_item', methods=['POST'])
def save_item():
    if not session.get('logged_in'):
        flash("Please log in to save items.", 'error')
        return redirect(url_for('log_in'))
    
    item = request.form.get('item')
    if item:
        db = get_db()
        db.execute("INSERT INTO saved_items (username, item) VALUES (?, ?)", (session['username'], item))
        db.commit()
        return redirect(url_for('saved_items'))  # Redirect to saved items page after saving

    flash("No item to save", 'error')
    return redirect(url_for('home'))

# Route to display saved items
@app.route('/saved_items')
def saved_items():
    if not session.get('logged_in'):
        flash("Please log in to view saved items.", 'error')
        return redirect(url_for('log_in'))
    
    db = get_db()
    cursor = db.execute("SELECT id, item FROM saved_items WHERE username = ?", (session['username'],))
    items = cursor.fetchall()  # Fetch items as a list of tuples (id, item)
    return render_template('saved_items.html', items=items)

@app.route('/remove_item', methods=['POST'])
def remove_item():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 403  # Unauthorized if not logged in

    data = request.get_json()
    item_id = data.get('item_id')

    if item_id:
        db = get_db()  # Ensure using the correct database connection
        db.execute("DELETE FROM saved_items WHERE id = ? AND username = ?", (item_id, session['username']))
        db.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': 'Invalid item ID'}), 400


if __name__ == '__main__':
    app.run(debug=True)
