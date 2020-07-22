# -*- coding: utf-8 -*-
from imageai.Detection.Custom import CustomObjectDetection

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("data2/models/mod4.h5") 
detector.setJsonPath("data2/json/detection_config.json")
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image="data2/train/images/Page_00008.jpg", output_image_path="Page_00008_1.jpg")
for detection in detections:
    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])


