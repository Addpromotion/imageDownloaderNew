from flask import Flask, request, render_template, redirect, url_for
import os
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = request.form.get('urls').split()
        folder = 'static/images'
        # Вызов скрипта для скачивания изображений
        subprocess.run(['python', 'downloader.py'] + urls)
        return redirect(url_for('images'))
    return render_template('index.html')

@app.route('/images')
def images():
    folder = 'static/images'
    images = os.listdir(folder)
    return render_template('images.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)