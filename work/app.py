import os
from flask import Flask, url_for, render_template, request, redirect, send_file, session, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def root():
    files = os.listdir("./static/uploaded_img/")
    aareturn send_file("./static/uploaded_img/" + request.form['img'], attachment_filename=request.form['img'], as_attachment=True)

if __name__ == '__main__':
    app.secret_key = "123123123"
    app.run(host='0.0.0.0', port=8080, debug=True)