# PCMI: Playing Card Manipulation Initiative
Full PCMI Codebase for CS2210 final project Fall 2024.

Group Members:

- Alexis Carey
- Aurelia Kornheiser
- Lila Sargent
- Tovahn Vitols

<br><br>

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

### Starting the game

Once all the players have connnected you may nagivate to the */admin* path and, assuming you are an admin user, press the start game button to beign a round.

### Managing the Database
- Add a new admin

    Enter the username of the user you would like to make a new admin in the [make_admin.sql](make_admin.sql) file and run the file in a SQL interface such as DB Browser

- Delete Guest Users

    In order to reduce the size of the database it is advantagous to routinely delete guest users. This may be accomplished by running the [DELETE_GUESTS.sql](DELETE_GUESTS.sql) file in a SQL interface such as DB Browser

### Physical Setup

Must be wired according to wiring diagram. *Full diagram and instructions to be added at a later date.*

---
<br><br>

# Attribution

Please refer to the [credits](credits.md) for all attribution and acknowledgements