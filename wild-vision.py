from pathlib import Path
from ultralytics import YOLO


model = YOLO("yolo_models/WAO_Split1_YOLOv8s_pretrained.engine")

result = model.predict(
	source = source, 
	name = name,
	save = False,
	save_txt = True,
	save_conf = True,
	imgsz = 640,
	conf = 0.25,
	stream = False,
	batch = -1,
)

