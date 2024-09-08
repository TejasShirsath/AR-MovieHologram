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

while True:
    success, frame = cap.read()
    movie_success, movie_frame = movie.read()

    window_height, window_width = frame.shape[:2]

    if movie_success:
        overlayFrame(frame, movie_frame, 200, 150, 50, 10)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
movie.release()
cv2.destroyAllWindows()
