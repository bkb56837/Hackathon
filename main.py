import base64
import cv2
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/upload/file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #imagestring = request.params('ImageData')
        #response = {'message': imagestring}
        #return jsonify(response)
        # check if the post request has the file part
        if 'image_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        image_file = request.files['image_file']
        # if user does not select file, browser also submit an empty part without filename
        if image_file.filename == '':
            flash('No selected image file')
            return redirect(request.url)
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)
            print('Uploaded image file')

            # do cool stuff with image (maybe better in a separate thread?)
            image = cv2.imread(file_path)
            filtered = cv2.bilateralFilter(image, 15, 150, 150)
            cv2.imwrite(file_path, filtered)

            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload/data', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        image_b64_data = request.form.get('data', '')
        print("Form data", image_b64_data)

        # decode image data and save to file
        image_data = base64.b64decode(image_b64_data.split(',')[1].encode())
        filename = 'image.png'
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'wb') as f:
            f.write(image_data)

        # do cool stuff with image (in a separate thread?)

        # create a JSON response and return to poster
        response = {
            "bounding_box":
                {
                    "x": 220,
                    'y': 200,
                    'width': 200,
                    'height': 60
                }
        }

        return jsonify(response)




#@app.route('/upload', methods=['GET', 'POST'])
#def upload_file():
 #   if request.method == 'POST':
  #      f = request.files['the_file']
  #      f.save('/var/www/uploads/uploaded_file.txt')
