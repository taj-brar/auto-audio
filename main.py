import pytesseract.pytesseract
from pycaw.pycaw import AudioUtilities
from PIL import ImageGrab, Image
from easyocr import easyocr

# CONSTANTS
MUTE_TIME = 5               # time at which music muted
SPOTIFY = "Spotify.exe"     # name of app to mute
LEFT_BOUNDARY = 0.4         # left boundary for cropping timer
RIGHT_BOUNDARY = 0.7        # right boundary for cropping timer
TOP_BOUNDARY = 0.0          # top boundary for cropping timer
BOTTOM_BOUNDARY = 0.1       # bottom boundary for cropping timer


# set tesseract path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Taj\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


# This method finds the Spotify app and mutes it
def mute_spotify(mute):
    # get all running apps
    sessions = AudioUtilities.GetAllSessions()

    # find spotify from list
    for session in sessions:
        if session.Process and session.Process.name() == SPOTIFY:
            # adjust volume
            volume = session.SimpleAudioVolume
            volume.SetMute(mute, None)


# This method uses the OCR library to read the time from the image
def get_time(img_name):
    # get time using ocr
    reader = easyocr.Reader(["en"], gpu=True)
    results = reader.readtext(img_name, allowlist="0123456789")

    return results[0][1]


# This method takes a screenshot of the screen and crops it to just the timer
def get_timer_img():
    # take screenshot of entire screen
    screen = ImageGrab.grab()

    # get dimensions of screen
    width, height = screen.size

    # get locations of bounding box of timer
    left = int(LEFT_BOUNDARY * width)
    right = int(RIGHT_BOUNDARY * width)
    top = int(TOP_BOUNDARY * height)
    bottom = int(BOTTOM_BOUNDARY * height)

    # crop image to get timer
    timer = screen.crop((left, top, right, bottom))
    timer.show()

    return timer


# This method repeatedly checks the timer to be below the threshold and mutes the app
def auto_adjust():
    # get time in seconds as an int
    seconds = int(get_time("a2.png"))
    print(seconds)

    # check if spotify should mute
    if seconds < MUTE_TIME:
        mute_spotify(True)
    else:
        mute_spotify(False)

# This method saves the screen as an img
def save_image():
    import time
    time.sleep(3)
    get_timer_img().save("a.png", "PNG")


# Repeatedly check the timer and auto adjust the audio
while True:
    auto_adjust()
