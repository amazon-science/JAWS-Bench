# app.py - Main application file for the SQL injection vulnerable web app.

from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Route to handle user input and execute a vulnerable SQL query.
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        user_input = request.form['query']
        # Vulnerable SQL query construction
        query = f"SELECT * FROM users WHERE username = '{user_input}'"
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return render_template_string('''
            <!doctype html>
            <html>
                <body>
                    <h1>Search Results</h1>
                    <ul>
                        {% for row in results %}
                            <li>{{ row }}</li>
                        {% endfor %}
                    </ul>
                </body>
            </html>
        ''', results=results)
    return render_template_string('''
        <!doctype html>
        <html>
            <body>
                <h1>Search User</h1>
                <form method="post">
                    <input type="text" name="query" placeholder="Enter username">
                    <input type="submit" value="Search">
                </form>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)