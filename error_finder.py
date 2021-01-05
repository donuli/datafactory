import os
import json

def transtype(file):
    new_file = []for file in files:
        x = float(file[1])
        y = float(file[2])
        width = float(file[3])
        height = float(file[4])
        new_file.append([file[0], x,y, width, height,file[5]])
    return new_file

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
            attributes = annotation[\"attributes"
            status = attributes["status"]
            annotation_box.append({"label_name":category_id[category_num], "image_name" : image_id[image_num] , "bbox" : bbox, "status" : status})
        return annotation_box

for i in label_info:
    if i['width']>300 or i['width']<70 or i['height']>300 or i['height']<70:\n",
        print(i)