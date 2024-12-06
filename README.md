# PCMI: Playing Card Manipulation Initiative
Full PCMI Codebase


# Instructions:

### Camera Recognition

To get the detection model working, download the repo, run `pip install ultralytics[export]`, and run `yolo.py`.

If you encounter an error similar to `qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.`, you'll need to reinstall `libxcb` via `sudo apt remove libxcb-xinerama0` and then `sudo apt install libxcb-xinerama0`.



### Main App

Simply runnning [app.py](app.py) should be sufficent to start all necessary services. 

Please change go.uvm.edu database entries to correct endpoint to ensure proper integration. 

Alternatively, change the value in [Constants.py](Constants.py)

### Authentication

Please change Google Authentication Client to the right endpoint.

# Attribution

Please refer to the [credits](credits.md) for all attribution and acknowledgements