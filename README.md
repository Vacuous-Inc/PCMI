# PCMI: Playing Card Manipulation Initiative
Full PCMI Codebase


To get the detection model working, download the repo, run `pip install ultralytics[export]`, and run `yolo.py`.
If you encounter an error similar to `qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.`, you'll need to reinstall `libxcb` via `sudo apt remove libxcb-xinerama0` and then `sudo apt install libxcb-xinerama0`.
