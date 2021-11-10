# web-app for API image manipulation
from flask import Flask, request, render_template, send_from_directory
import os
from PIL import Image
import cv2
from werkzeug.utils import redirect
import process as process

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# default access page
@app.route("/")
def main():
    return render_template('proses.html')

# upload selected image and forward to processing page
@app.route("/proses1", methods=['POST'])
def proses1():
    target = os.path.join(APP_ROOT, 'static/images/')
    filename = request.files['file']
    print('filename : ',filename)

    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # save file
    data = os.path.join(target, "query.jpg")
    filename.save(data)
    #img = cv2.imread(data, cv2.IMREAD_GRAYSCALE)
    img=data
    print(img)
    # check mode
    if 'gauss_adaptive' in request.form.get('select_thresholding'):
        mode = 'gauss_adaptive'
    elif 'laplacian_convolution' in request.form.get('select_thresholding'):
        mode = 'laplacian_convolution'
    elif 'sobel_x_y' in request.form.get('select_thresholding'):
        mode = 'sobel_x_y'

    #process
    if mode == 'gauss_adaptive':
        img_res = process.gaussian_adaptive_thresh(img)
        cv2.imwrite("/".join([target, 'result.jpg']),img_res)
        data = 'Gaussian Adaptive Thresholding'
    elif mode == 'laplacian_convolution':
        img_res = process.laplacian_convolution(img)
        cv2.imwrite("/".join([target, 'result.jpg']),img_res)
        data = 'Laplacian Convolution'
    elif mode == 'sobel_x_y':
        img_res = process.sobel_x_y(img)
        cv2.imwrite("/".join([target, 'result.jpg']),img_res)
        data = 'Sobel X & Y'
    # forward to processing page
    return render_template('proses.html', data=data)

# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)

if __name__ == "__main__":
    app.run(debug=True)