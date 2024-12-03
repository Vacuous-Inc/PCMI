import cv2
from picamera2 import Picamera2
from ultralytics import YOLO


# Set up the camera with Picam
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 640)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load model
model = YOLO("pcmi_ncnn_model") # "pcmi_model.pt" or "pcmi_ncnn_model" (ncnn is faster)

# function to capture a single frame, analyze it, and return card results
def get_cards():
    # Capture a frame from the camera
    frame = picam2.capture_array()

    # Run YOLO model on the captured frame and store the results
    results = model(frame, imgsz=160)

    # add names to an array and return it
    names = model.names
    cards = []
    for r in results[0].boxes.cls:
        cards.append(names[int(r)])
    return cards


# if program is being run alone, analyze every frame and display output in gui
if __name__ == "__main__":
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Run YOLO model on the captured frame and store the results
        results = model(frame, imgsz = 160)

        # Output the visual detection data, we will draw this on our camera preview window
        annotated_frame = results[0].plot()

        # Get inference time
        inference_time = results[0].speed['inference']
        fps = 1000 / inference_time  # Convert to milliseconds
        text = f'FPS: {fps:.1f}'

        # Define font and position
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, 1, 2)[0]
        text_x = annotated_frame.shape[1] - text_size[0] - 10  # 10 pixels from the right
        text_y = text_size[1] + 10  # 10 pixels from the top

        # Draw the text on the annotated frame
        cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow("Camera", annotated_frame)

        # Exit the program if q is pressed
        if cv2.waitKey(1) == ord("q"):
            break

    # Close all windows
    cv2.destroyAllWindows()

