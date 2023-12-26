from flask import Flask, render_template, request, redirect
import string
import random

app = Flask(__name__)

# Dictionary to store mappings of short alias to long URL
url_mapping = {}

def generate_short_alias():
    # Generate a random 6-character alias using letters and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('long_url')
    
    # Check if the URL is already shortened
    short_alias = next((alias for alias, url in url_mapping.items() if url == long_url), None)

    if not short_alias:
        # Generate a new short alias
        short_alias = generate_short_alias()
        url_mapping[short_alias] = long_url

    short_url = request.url_root + short_alias
    return render_template('result.html', long_url=long_url, short_url=short_url)

@app.route('/<short_alias>')
def redirect_to_original(short_alias):
    long_url = url_mapping.get(short_alias)
    if long_url:
        return redirect(long_url)
    else:
        return render_template('error.html', message='URL not found')

if __name__ == '__main__':
    app.run(debug=True)
