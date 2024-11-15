import cv2

# Load the video
video_path = r"C:\Users\tanse\Downloads\6387-191695740_small.mp4"
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read the first frame
ret, frame = cap.read()

if not ret:
    print("Error: Couldn't read the video frame.")
    exit()

# Select a region to track (initialize with the first frame)
bbox = cv2.selectROI("Select Person", frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

# Create a tracker object (CSRT is a robust tracker for real-time object tracking)
tracker = cv2.legacy.TrackerCSRT_create()  # Updated to legacy module

# Initialize the tracker with the first frame and the bounding box
tracker.init(frame, bbox)

# Zoom factor, initial value is 1 (no zoom)
zoom_factor = 1.0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Update the tracker and get the updated position of the bounding box
    success, bbox = tracker.update(frame)

    # Draw the bounding box if the tracking is successful
    if success:
        p1 = (int(bbox[0]), int(bbox[1]))  # Top-left corner
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))  # Bottom-right corner
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)  # Green rectangle around the person

        # Zoom effect based on zoom_factor
        if zoom_factor != 1.0:
            x, y, w, h = [int(v) for v in bbox]
            # Crop the region of interest (ROI)
            cropped = frame[y:y+h, x:x+w]
            
            # Apply zoom effect: Resize the cropped region by zoom_factor
            zoomed_frame = cv2.resize(cropped, None, fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_LINEAR)
            
            # Make sure the zoomed region fits back into the original frame size
            # Center the zoomed region
            zoomed_height, zoomed_width = zoomed_frame.shape[:2]
            y_offset = max(0, (frame.shape[0] - zoomed_height) // 2)
            x_offset = max(0, (frame.shape[1] - zoomed_width) // 2)

            # Place the zoomed-in region back to the original frame size
            frame[y_offset:y_offset+zoomed_height, x_offset:x_offset+zoomed_width] = zoomed_frame

    else:
        cv2.putText(frame, "Tracking failure", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame with the tracking result
    cv2.imshow("Tracking", frame)

    # Check for keypresses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Exit on 'q'
        break
    elif key == ord('a'):  # Zoom in on 'a'
        zoom_factor += 0.1  # Increase zoom factor
    elif key == ord('b'):  # Reset zoom on 'b'
        zoom_factor = 1.0  # Reset zoom to original size

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
