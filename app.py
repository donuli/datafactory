import os
import csv
import json
import numpy as np
from flask import Flask, url_for, render_template, request, redirect, send_file, session, send_file
from werkzeug.utils import secure_filename
import pymysql

def annotation(categories,images,annotations):
    category_id={}
    image_id={}
    annotation_box=[]
    
    for category in categories:
        category_id[category["id"]]=category["name"]
    
    for image in images:
        image_id[image["id"]]=image["file_name"]
    
    for annotation in annotations:
        category_num = annotation["category_id"]
        image_num = annotation["image_id"]
        bbox = annotation["bbox"]
        attributes = annotation["attributes"]
        status = attributes["status"]
        annotation_box.append({"label_name":category_id[category_num], "image_name" : image_id[image_num] , "bbox" : bbox, "status" : status})
    return annotation_box

def annotation(categories,images,annotations):
    category_id={}
    image_id={}
    annotation_box=[]

    for category in categories:
        category_id[category["id"]]=category["name"]

    for image in images:
        image_id[image["id"]]=image["file_name"]

    for annotation in annotations:
        category_num = annotation["category_id"]
        image_num = annotation["image_id"]
        bbox = annotation["bbox"]
        attributes = annotation["attributes"]
        status = attributes["status"]
        annotation_box.append({"label_name":category_id[category_num], "image_name" : image_id[image_num] , "bbox" : bbox, "status" : status})
    return annotation_box

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def root():
    return render_template('index.html')

@app.route('/sign-in-do', methods=['GET', 'POST'])
def sign_in_do():
    if request.method == 'POST':
        data = [request.form['username'], request.form['password']]
        conn = pymysql.connect(host='172.29.0.3', user='root',
                               password='han5100', db='userinfo')
        curs = conn.cursor()
        sql = 'select username,password from USER'
        curs.execute(sql)
        output = curs.fetchall()
        userinfo = []
        for i in range(len(output)):
            username = output[i][0]
            password = output[i][1]

            userinfo.append([username, password])
        try:
            if data in userinfo:
                session['logged_in'] = True
                return redirect('/')
            else:
                return 'Retry'
        except:
            return 'retry'
    conn.close()

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    return render_template('signUp.html')

@app.route('/sign-up-do', methods=['GET', 'POST'])
def sign_up_do():
    if request.method == 'POST':
        data = [request.form['username'],
                request.form['password'], request.form['email']]
        conn = pymysql.connect(host='172.29.0.3', user='root',
                               password='han5100', db='userinfo')
        curs = conn.cursor()

        sql = 'select username from USER'
        curs.execute(sql)
        output = curs.fetchall()
        userinfo = []
        for i in range(len(output)):
            username = output[i][0]
            userinfo.append(username)

        if data[0] in userinfo:
            return 'already create'
        else:
            sql = 'insert into USER (username,password,email) value (%s, %s, %s)'
            curs.execute(sql, data)
            conn.commit()
        conn.close()
        return render_template('index.html')

@app.route('/imageData', methods=['GET', 'POST'])
def image_data():
    i_files=[]
    v_files=[]
    i_count = len(i_files)
    v_count = len(v_files)
    files = os.listdir("./static/uploaded_img/share/")
    for file in files:
        if ".png" in file:
            i_files.append(file)
        elif ".mp4" in file:
            v_files.append(file)
    return render_template('image.html',i_files=i_files, v_files=v_files,i_count=i_count,v_count=v_count)

@app.route('/image-up-do', methods=['GET', 'POST'])
def image_up_do():
    files = os.listdir("./static/uploaded_img/share/")
    if request.method == 'POST':
        images = request.files.getlist('image[]')
        for image in images:
            if image in files:
                continue
            image.save('./static/uploaded_img/share/' + secure_filename(image.filename))
        return 'Image upload success!'
    else:
        return render_template('page_not_found.html')

@app.route('/image-down-do', methods=['GET', 'POST'])
def image_down_do():
    if request.method == 'POST':
        files = os.listdir("./static/uploaded_img/share/")
        for file in files:
            if file == request.form['img']:
                return send_file("./static/uploaded_img/share/" + request.form['img'], attachment_filename=request.form['img'], as_attachment=True)
    else:
        return 'no search file...'

@app.route('/labelData',methods = ['GET','POST'])
def label_data():
    files = os.listdir("./static/uploaded_csv/")
    count = len(files)
    return render_template('label.html',files=files,count=count)

@app.route('/csv-up-do', methods=['GET', 'POST'])
def csv_up_do():
    files = os.listdir("./static/uploaded_csv/")
    if request.method == 'POST':
        csvs = request.files.getlist('csv[]')
        for csv in csvs:
            if csv in files:
                continue
            csv.save('./static/uploaded_csv/' + secure_filename(csv.filename))
        return 'CSV upload success!'
    else:
        return render_template('page_not_found.html')

@app.route('/csv-down-do', methods=['GET', 'POST'])
def csv_down_do():
    if request.method == 'POST':
        files = os.listdir("./static/uploaded_csv")
        for file in files:
            if file == request.form['csv']:
                return send_file("./static/uploaded_csv/" + request.form['csv'], attachment_filename=request.form['csv'], as_attachment=True)

    else:
        return 'no search file...'
    return ''

@app.route('/dataSet',methods = ['GET','POST'])
def data_set():
    files = os.listdir("./static/uploaded_csv")
    datas =[]
    conn = pymysql.connect(host='172.29.0.3', user='root',
                            password='han5100', db='data')
    curs = conn.cursor()
    sql = 'select * from DATA'
    curs.execute(sql)
    output = curs.fetchall()
    for n in range(len(output)):
        image = output[n][1]
        x_min = output[n][2]
        y_min = output[n][3]
        x_max = output[n][4]
        y_max = output[n][5]
        label = output[n][6]
        datas.append({'image':image,'x_min':x_min,'y_min':y_min,'x_max':x_max,'y_max':y_max,'label':label })
    conn.close()
    count = len(datas)
    count_csv = len(files)

    return render_template('dataset.html',files=files,datas=datas,count=count,count_csv=count_csv)

@app.route('/input-db', methods=['GET', 'POST'])
def input_db_do():
    if request.method == 'POST':
        files = os.listdir("./static/uploaded_csv")
        file = request.form['csv']
        if file in files:
            filename = open(f"./static/uploaded_csv/{file}", 'r',encoding='utf-8')
            json_data = json.load(filename)
            categories = json_data["categories"]
            images = json_data["images"]
            annotations = json_data["annotations"]
            label_info=[]
            for i in annotation(categories,images,annotations):
                box = i["bbox"]
                label_info.append({"image": i["image_name"], "x":box[0], "y":box[1], "width":box[2], "height":box[3], "label":i["label_name"]+"_"+i["status"]})
            
            conn = pymysql.connect(host='172.29.0.3', user='root', password='han5100', db='data')
            curs = conn.cursor()
            for row in label_info[:]:
                image_name = (row["image"])
                x_min = (row["x"])
                y_min = (row["y"])
                x_max = (row["width"])
                y_max = (row["height"])
                label = (row["label"])
                sql = "insert into DATA (image, x, y, width, height, label) value ( %s, %s, %s, %s, %s, %s)"
                curs.execute(
                    sql, (image_name, x_min, y_min, x_max, y_max, label))

                conn.commit()       
            filename.close()    
            conn.close()
            return 'DB write success!!'
        else:
            return 'Failed...'

@app.route('/export', methods=['GET', 'POST'])
def export_do():
    if request.method == 'POST':
        conn = pymysql.connect(host='172.29.0.3', user='root',
                               password='han5100', db='data')
        curs = conn.cursor()
        sql = 'select * from DATA'
        curs.execute(sql)
        output = curs.fetchall()
        file = open("dataset.csv", mode='w',encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(["image", "x", "y", "width", "height", "label"])
        for item in output:
            writer.writerow([item[1],item[2],item[3], item[4],item[5],item[6]])
            print(item)
        conn.close()
        file.close()
        return send_file('./dataset.csv',attachment_filename='dataset.csv',as_attachment=True)
    else:
        return render_template('retry')
    
@app.route('/size_val', methods=['GET', 'POST'])
def size_error():
    error_file = []
    files = os.listdir("./static/uploaded_csv/")
    count = len(files)
    if request.method == 'POST':
        files = os.listdir("./static/uploaded_csv/")
        for file in files:
            if file == request.form['csv']:
                filename = open(f"./static/uploaded_csv/{file}",'r',encoding='UTF-8')
                json_data = json.load(filename)
                categories = json_data["categories"]
                images = json_data["images"]
                annotations = json_data["annotations"]
                label_info=[]
                for i in annotation(categories,images,annotations):
                    box = i["bbox"]
                    label_info.append({"image": i["image_name"], "x":box[0], "y":box[1], "width":box[2], "height":box[3], "label":i["label_name"]+"_"+i["status"]})
                for i in label_info:
                    if i['width']>300 or i['width']<70 or i['height']>300 or i['height']<70:
                        error_file.append(i)
    return render_template('sizeError.html',files=files,count=count,error_file=error_file)
    
#@app.route('/area', methods=['GET', 'POST'])
#def area_error():

@app.route("/sign-out")
def sign_out():
    """Logout Form"""
    session['logged_in'] = False
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = "123123123"
    app.run(host='0.0.0.0', port=8080, debug=True)