import cv2 as cv
import tkinter as tk
from PIL import Image
from PIL import ImageTk

video = cv.VideoCapture(0)
app = tk.Tk()
display = tk.Label(app)
display.pack()

def open_camera():
    _, frame = video.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame = cv.putText(frame, '[*]', (50, 150), cv.FONT_HERSHEY_PLAIN, 5.0, (255, 255, 255), 4)
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(frame)
    display.photo_image = frame
    display.configure(image=frame)
    display.after(10, open_camera)

start_capture_button = tk.Button(app, text='Pobierz obraz', command=open_camera)
start_capture_button.pack()

app.mainloop()
