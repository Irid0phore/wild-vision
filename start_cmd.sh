sudo docker run -it --ipc=host -v /home/alx/wild-vision:/mnt/wild-vision --runtime=nvidia ultralytics/ultralytics:latest-jetson-jetpack4
cd /mnt/wild-vision; python3 wild-vision.py
