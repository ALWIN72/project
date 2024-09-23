from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

images = []  # List to store image file names and notes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        note = request.form['note']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            images.append({'filename': file.filename, 'note': note})
        return redirect(url_for('index'))

    return render_template('index.html', images=images)

@app.route('/delete/<filename>')
def delete(filename):
    # Remove image from the uploads directory and the images list
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    global images
    images = [img for img in images if img['filename'] != filename]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
