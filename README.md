# PCMI: Playing Card Manipulation Initiative
Full PCMI Codebase


Resources used for detection model
- [Getting Started with YOLO](https://core-electronics.com.au/guides/getting-started-with-yolo-object-and-animal-recognition-on-the-raspberry-pi/)
- [Playing Card Detection Tutorial](https://medium.com/@sdwiulfah/having-fun-with-yolov8-how-good-your-model-in-detecting-playing-card-a468a02e4775) and [Codebase](https://github.com/saskia-dwi-ulfah/playing-card-detection-yolov8/)
- [Playing Card Training Dataset](https://www.kaggle.com/datasets/andy8744/playing-cards-object-detection-dataset)
- [Ultralytics Documentation](https://docs.ultralytics.com/)
- [PiCamera2 Documentation](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)

To get the detection model working, download the repo, run `pip install ultralytics[export]`, and run `yolo.py`.
If you encounter an error similar to `qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.`, you'll need to reinstall `libxcb` via `sudo apt remove libxcb-xinerama0` and then `sudo apt install libxcb-xinerama0`.
