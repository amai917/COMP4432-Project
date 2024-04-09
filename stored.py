from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
messages = []
xss_detected = False

@app.route('/', methods=['GET', 'POST'])
def home():
    global xss_detected
    # Post messages in the blog post site with current date
    if request.method == 'POST':
        message_content = request.form['message']
        message = {
            'content': message_content,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        # Messages would be deteremined whether or not it is a script or not
        if '<script>' in message['content'].lower():
            # True if message is in <script> and window will pop up
            xss_detected = True
        else:
            # False if not so window would not pop and it will just post
            xss_detected = False
        messages.append(message)
        return redirect(url_for('home'))
    return render_template('index.html', messages=messages, xss_detected=xss_detected)

# Content Security Policy line must be commented out to disable CSP
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self';"
    return response

if __name__ == '__main__':
    app.run(debug=True)
