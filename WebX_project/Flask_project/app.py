from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
import joblib
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/personality_db"
mongo = PyMongo(app)

# Configure Flask-Mail (SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "2022.chirag.choudhary@ves.ac.in"
app.config['MAIL_PASSWORD'] = "dizrqxwgzbjtbicq"
mail = Mail(app)

# Load ML Model
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
print("✅ Model loaded successfully!")
print("Model Type:", type(model))

# Generate and send OTP
def send_otp(email):
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    session['email'] = email
    msg = Message('Your OTP Code for PersonalityPredict.AI', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Your OTP code is {otp}. Use this to complete your registration/login.'
    mail.send(msg)
    return otp

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        user = mongo.db.users.find_one({"email": email})
        if user:
            flash("Email already registered! Please login.", "danger")
            return redirect(url_for('login'))
        send_otp(email)
        return redirect(url_for('verify_otp', action='signup'))
    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = mongo.db.users.find_one({"email": email})
        if not user:
            flash("Email not registered! Please sign up.", "danger")
            return redirect(url_for('signup'))
        send_otp(email)
        return redirect(url_for('verify_otp', action='login'))
    return render_template('login.html')

# OTP Verification Route
@app.route('/verify_otp/<action>', methods=['GET', 'POST'])
def verify_otp(action):
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            email = session.get('email')
            if action == 'signup':
                mongo.db.users.insert_one({"email": email})
            session.pop('otp', None)
            session['logged_in'] = True
            session['email'] = email
            flash("Verification successful!", "success")
            return redirect(url_for('predict'))
        else:
            flash("Invalid OTP. Try again!", "danger")
    return render_template('verify_otp.html', action=action)

# Landing Page Route
@app.route('/')
def landing():
    return render_template('landing.html')

# Get Personality Quote Based on Prediction
def get_personality_quote(personality_type):
    with open("personality_quotes.txt", "r", encoding="utf-8") as file:
        quotes = file.read().strip().split("\n")

    if personality_type == "extrovert":
        filtered_quotes = quotes[:8]
    elif personality_type == "introvert":
        filtered_quotes = quotes[8:16]
    else:
        filtered_quotes = quotes[16:]

    return random.choice(filtered_quotes)

# Prediction Page Route
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'logged_in' not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for('signup'))
    return render_template('predict.html')

# API Prediction Route
@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'Please enter some text to analyze!'})

    try:
        # Predict personality using the model
        transformed_text = vectorizer.transform([text])
        prediction = model.predict_proba(transformed_text)[0]
        introvert_prob, extrovert_prob = prediction[0], prediction[1]
        personality_type = (
            "ambivert" if abs(introvert_prob - extrovert_prob) < 0.1
            else "extrovert" if extrovert_prob > introvert_prob
            else "introvert"
        )
        
        # Get a personality quote
        quote = get_personality_quote(personality_type)

        return jsonify({
            'personality_type': personality_type.capitalize(),
            'quote': quote
        })

    except Exception as e:
        return jsonify({'error': str(e)})

# Logout Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True)
