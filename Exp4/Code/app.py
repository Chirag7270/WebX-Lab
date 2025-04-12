from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return '''<h1>Welcome to Flask App</h1>
              <p><a href="{}">Go to Profile</a></p>
              <p><a href="{}">Submit Data</a></p>
           '''.format(url_for('profile', username='User'), url_for('submit'))

@app.route('/profile/<username>')
def profile(username):
    return f'<h2>Profile Page</h2><p>Welcome, {username}!</p>'

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        return f'<h2>Submission Successful</h2><p>Name: {name}</p><p>Age: {age}</p>'
    return '''<form method="POST">
                  Name: <input type="text" name="name" required><br>
                  Age: <input type="number" name="age" required><br>
                  <input type="submit" value="Submit">
              </form>'''

if __name__ == '__main__':
    app.run(debug=True)
