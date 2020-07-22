# -*- coding: utf-8 -*-
from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="data1")
trainer.evaluateModel(model_path="data1/models/mod3.h5", json_path="data1/json/detection_config.json", iou_threshold=0.5, object_threshold=0.3, nms_threshold=0.5)

