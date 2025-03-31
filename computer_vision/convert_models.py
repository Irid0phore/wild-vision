from ultralytics import YOLO

model = YOLO("WAO_Split1_YOLOv8s_pretrained.pt")
model.export(format="engine")

model = YOLO("WAO_Split2_YOLOv8s_pretrained.pt")
model.export(format="engine")

model = YOLO("WAO_Split3_YOLOv8s_pretrained.pt")
model.export(format="engine")
