import gphoto2 as gp
import time


camera = gp.Camera()
camera.init()
summary = camera.get_summary()
summary = summary.text.split("\n")[:4]
print(f"Found camera model: {summary[1]}")
print()
print('Capturing image')

for i in range(10):
	t1 = time.time()
	
	file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
	print(f"Camera file path: {file_path.folder}/{file_path.name}")

	target_path = f"/home/alx/wild-vision/captures/{file_path.name}"
	print(f"Copying image to {target_path}")
	camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
	camera_file.save(target_path)
	
	t2 = time.time()
	print(f"Duration: {t2 - t1}")

	time.sleep(1)

camera.exit()
