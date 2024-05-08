"""
Moduł zawierający interfejs graficzny użytkownika zrealizowany przy pomocy modułu TKinter. 
Będzie on odpowiadał za obsługę interakcji z użytkownikiem, odtwarzanie dźwięków 
ostrzegawczych czy prezentowanie przetworzonego obrazu z kamery, który odbierać będzie 
z silnika przetwarzania obrazu. Jego częścią będą również menu służące do zmiany aktualnej 
konfiguracji systemu. 
"""
import tkinter as tk

import cv2 as cv
from cv2.typing import MatLike
import numpy as np
from PIL import Image
from PIL import ImageTk

from backup_camera.application import Application
from backup_camera._image_processing.image_porcessor import ImageProcessingEngine


class UserInteface:
    def __init__(self, parent_application: Application, video_source: ImageProcessingEngine) -> None:
        self._window = tk.Tk()
        self._window.title('Backup Camera')
        self._window.geometry('1280x720')
        self._window.resizable(False, False)
        
        self._event_handler = parent_application
        self._video_source = video_source
        
        self._menubar = tk.Menu(master=self._window)
        
        self._mode_menu = tk.Menu(master=self._menubar, tearoff=0)
        self._selected_camera_mode = tk.IntVar()
        self._selected_camera_mode.set(0)
        self._mode_menu.add_radiobutton(
            label='Park assistant', 
            variable=self._selected_camera_mode, 
            value=0,
            command=self._enable_park_assistant
        )
        self._mode_menu.add_radiobutton(
            label='Rearview mirror', 
            variable=self._selected_camera_mode, 
            value=1,
            command=self._enable_mirrow
        )
        self._mode_menu.add_radiobutton(
            label='Configuration', 
            variable=self._selected_camera_mode, 
            value=2,
            command=self._enable_config_mode
        )
        self._menubar.add_cascade(menu=self._mode_menu, label='Mode')
        
        self._window.config(menu=self._menubar)
        
        self._display = tk.Label(master=self._window)
        self._display.pack(fill='both')
    
    def _enable_mirrow(self):
        if self._menubar.index('end') > 1:
            self._menubar.delete(self._menubar.index('end'))
    
    def _enable_park_assistant(self):
        if self._menubar.index('end') > 1:
            self._menubar.delete(self._menubar.index('end'))
    
    def _enable_config_mode(self):
        if self._selected_camera_mode.get() != 2:
            return
        if self._menubar.index('end') > 1:
            self._menubar.delete(self._menubar.index('end'))
        
        self._config_menu = tk.Menu(master=self._menubar, tearoff=0)
        self._config_menu.add_checkbutton(label='Debug mode')
        self._config_menu.add_separator()
        self._config_menu.add_command(
            label='Select source',
            command=self._event_handler.set_source
        )
        self._config_menu.add_command(
            label='Image properties', 
            command=self._event_handler.set_image_properties
        )
        self._config_menu.add_separator()
        self._config_menu.add_checkbutton(label='Guidlines hidden')
        self._config_menu.add_command(
            label='Guidelines properties', 
            command=self._event_handler.set_guidelines_properties
        )
        self._config_menu.add_separator()
        self._config_menu.add_checkbutton(label='Mute sounds')
        self._config_menu.add_separator()
        self._config_menu.add_command(
            label='Detection properties',
            command=self._event_handler.set_detection_properties
        )
        self._menubar.add_cascade(menu=self._config_menu, label='Configuration')
    
    def show(self) -> None:
        self._updateVideoFrame(self._video_source.process_next_frame())
        self._window.mainloop()
    
    def _updateVideoFrame(self, video_frame: MatLike):
        if video_frame is None or video_frame.shape[1] != 1280 or video_frame.shape[0] != 720:
            video_frame = UserInteface.generate_placeholder_image()
        video_frame = ImageTk.PhotoImage(Image.fromarray(video_frame))
        self._display.photo_image = video_frame
        self._display.configure(image=video_frame)
        self._display.after(10, lambda frame=self._video_source.process_next_frame(): self._updateVideoFrame(frame))
        
    @staticmethod
    def generate_placeholder_image() -> MatLike:
        image = np.full((720, 1280), 0, dtype=np.uint8)
        image = cv.putText(
            img=image, 
            text='<NO VIDEO TO DISPLAY>', 
            org=(160, 370), 
            fontFace=cv.FONT_HERSHEY_PLAIN, 
            fontScale=5, 
            color=(255, 255, 255), 
            thickness=4
        )
        return image
