import os
import cv2
from pathlib import Path
from ultralytics import YOLO

def get_tile_ranges(img_shape, tile_size=640, tile_overlap=0.5):
	H, W = img_shape[0], img_shape[1]
	w, h = tile_size, tile_size
	x = (W - w * tile_overlap) / (w - w * tile_overlap)
	y =  (H - h * tile_overlap) / (h - h * tile_overlap)
	x, y = int(round(x)), int(round(y))
	
	tiles = np.zeros((x * y, 4)).astype(int);
	tile_idx = 0;
	for xOff in np.linspace(0, W-w, x).round().astype(int):
		for yOff in np.linspace(0, H-h, y).round().astype(int):
			tiles[tile_idx,:] = [xOff, yOff, xOff+w, yOff+h]
			tile_idx += 1

	return tiles

def run(model, img_file):
	img = cv2.imread(img_file)

	tile_ranges = get_tile_ranges(img.shape)

	result = model.predict(
		source = [img[xmin:xmax, ymin:ymax] for xmin, ymin, xmax, ymax in tile_ranges], 
		name = img_file.name,
		save = False,
		save_txt = True,
		save_conf = True,
		imgsz = 640,
		conf = 0.25,
		stream = False,
		batch = -1,
	)

model = YOLO("yolo_models/WAO_Split1_YOLOv8s_pretrained.engine")

src_folder = Path("~/wild-vision/captures")
dir_list = os.listdir(str(src_folder))
captures = [x for x in dir_list if x.startswith("capt")]

for capture in captures:
	img_file = src_folder / capture
	run(model, img_file)
