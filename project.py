import cv2
import time
from ffpyplayer.player import MediaPlayer
import threading

cap = cv2.VideoCapture(0)

globalFrame = None
globalFrameLock = threading.Lock()
x, y = 10, 10  # Variables for overlay position
overlayActive = True  # Flag to check if overlay video is active
pause = False  # Global pause variable

def overlayFrame(videoFile, frameWidth, frameHeight):
    global globalFrame, overlayActive, pause
    video = cv2.VideoCapture(videoFile)
    player = MediaPlayer(videoFile)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_time = 1 / fps

    while True:
        start_time = time.time()

        # Respect the global pause state
        if not pause:
            ret, frame = video.read()
            if not ret:
                # Set flag to False when video ends
                overlayActive = False
                break

            resizedFrame = cv2.resize(frame, (frameWidth, frameHeight))
            with globalFrameLock:
                globalFrame = resizedFrame

        # Pause or resume the audio when pause is toggled
        player.set_pause(pause)

        # Audio frame synchronization
        audio_frame, val = player.get_frame()
        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame

        # Wait to maintain synchronization
        elapsed_time = time.time() - start_time
        if elapsed_time < frame_time:
            time.sleep(frame_time - elapsed_time)

    video.release()
    player.close_player()
    globalFrame = None


def main():
    global globalFrame, overlayActive, pause
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.resize(frame, (1000, 500))

        # Overlay the video frame onto the camera feed
        with globalFrameLock:
            if globalFrame is not None and overlayActive:
                frame[y:y + globalFrame.shape[0], x:x + globalFrame.shape[1]] = globalFrame

        cv2.imshow('Camera with Overlay', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            pause = not pause  # Toggle the pause state

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    thread1 = threading.Thread(target=main)
    thread2 = threading.Thread(target=overlayFrame, args=('demo.mp4', 200, 200))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()