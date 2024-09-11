import cv2

# camera variables 
mobileCamera = "http://192.168.1.100:8080/video"
laptopCamera = 0
camera = laptopCamera

# Load the movie and the camera feed
movie = cv2.VideoCapture('demo.mp4')
cap = cv2.VideoCapture(camera)

# Resize the window
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', (1000, 500))

# Functions to calculate coordinates
def x_axis(percent):
    return int(percent * window_width / 100)

def y_axis(percent):
    return int(percent * window_height / 100)

# Function to overlay movie frame
def overlayFrame(frame, smallFrame, frameWidth, frameHeight, x, y):
    smallFrame_resized = cv2.resize(smallFrame, (frameWidth, frameHeight))
    movie_height, movie_width = smallFrame_resized.shape[:2]
    x_offset = int(x * window_width / 100)
    y_offset = int(y * window_height / 100)
    frame[y_offset:y_offset+movie_height, x_offset:x_offset+movie_width] = smallFrame_resized

# Variable to control pause and play of the movie
overlay_paused = False

while True:
    success, frame = cap.read()
    window_height, window_width = frame.shape[:2]
    
    # Read the movie frame only if not paused
    if not overlay_paused:
        movie_success, movie_frame = movie.read()

    # Overlay movie frame if not paused and movie frame exists
    if movie_success and movie_frame is not None:
        overlayFrame(frame, movie_frame, 200, 150, 50, 10)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        overlay_paused = not overlay_paused  # Toggle pause/play when 'P' is pressed

cap.release()
movie.release()
cv2.destroyAllWindows()
