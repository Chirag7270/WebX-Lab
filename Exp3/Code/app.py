from flask import Flask, request, render_template

app = Flask(__name__)

# Homepage route
@app.route('/')
def home():
    name = request.args.get('name', 'Guest')
    return f"Welcome, {name}! <br><a href='/contact'>Go to Contact Form</a>"

# Contact form route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return render_template('thank_you.html', name=name, email=email)
    return render_template('contact.html')

# Thank You route
@app.route('/thank_you')
def thank_you():
    return "Thank you for submitting your details!"

if __name__ == '__main__':
    app.run(debug=True)