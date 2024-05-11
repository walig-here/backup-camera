"""
Moduł zawierający interfejs graficzny użytkownika zrealizowany przy pomocy modułu TKinter. 
Będzie on odpowiadał za obsługę interakcji z użytkownikiem, odtwarzanie dźwięków 
ostrzegawczych czy prezentowanie przetworzonego obrazu z kamery, który odbierać będzie 
z silnika przetwarzania obrazu. Jego częścią będą również menu służące do zmiany aktualnej 
konfiguracji systemu. 
"""
import tkinter as tk
from tkinter import filedialog

import cv2 as cv
from cv2.typing import MatLike
import numpy as np
from PIL import Image
from PIL import ImageTk

from backup_camera.application import Application
from backup_camera._image_processing.image_porcessor import ImageProcessingEngine
from backup_camera._image_receiver import ImageReceiver


class UserInteface:
    def __init__(self, display_size: tuple[int, int], parent_application: Application, 
                 video_source: ImageProcessingEngine) -> None:
        self._window = tk.Tk()
        self._window.title('Backup Camera')
        self._window.geometry(f'{display_size[0]}x{display_size[1]}')
        self._window.resizable(False, False)
        
        self._event_handler = parent_application
        self._video_source = video_source
        self._display_size = (display_size[1], display_size[0])
        self._guidelines_hidden = tk.BooleanVar(value=False)
        self._mute_sounds = tk.BooleanVar(value=False)
        
        self._menubar = tk.Menu(master=self._window)
        self._init_camera_mode_menu()
        self._init_source_menu()
        self._window.config(menu=self._menubar)
        
        self._display = tk.Label(master=self._window)
        self._display.pack(fill='both')
    
    def _enter_mirror_mode(self):
        self._reload_default_menu_bar_layout()
    
    def _enter_park_assistant_mode(self):
        self._reload_default_menu_bar_layout()
    
    def _enter_config_mode(self):
        self._reload_default_menu_bar_layout()
        
        self._config_menu = tk.Menu(master=self._menubar, tearoff=0)
        self._config_menu.add_command(
            label='Image properties', 
            command=self._event_handler.set_image_properties
        )
        self._config_menu.add_separator()
        self._config_menu.add_checkbutton(
            label='Guidlines hidden',
            variable=self._guidelines_hidden,
            command=self._event_handler.change_guidelines_visibility
        )
        self._config_menu.add_command(
            label='Guidelines properties', 
            command=self._event_handler.set_guidelines_properties
        )
        self._config_menu.add_separator()
        self._config_menu.add_checkbutton(
            label='Mute sounds',
            variable=self._mute_sounds,
            command=self._event_handler.change_mute_sounds
        )
        self._config_menu.add_separator()
        self._config_menu.add_command(
            label='Detection properties',
            command=self._event_handler.set_detection_properties
        )
        self._menubar.add_cascade(menu=self._config_menu, label='Configuration')
    
    def _reload_default_menu_bar_layout(self):
        if self._menubar.index('end') > 2:
            self._menubar.delete(self._menubar.index('end'))
    
    def _init_source_menu(self):
        self._source_menu = tk.Menu(master=self._menubar, tearoff=0)
        self._selected_source_index = tk.IntVar()
        
        sources = ImageReceiver.get_available_sources()
        for source_name in sources:
            self._source_menu.add_radiobutton(
                label=source_name, 
                variable=self._selected_source_index, 
                value=sources[source_name],
                command=lambda source_index=sources[source_name]: self._event_handler.set_source(source_index)
            )
            
        self._selected_source_index.set(-2)
        self._menubar.add_cascade(menu=self._source_menu, label='Source')
        
    
    def _init_camera_mode_menu(self):
        self._mode_menu = tk.Menu(master=self._menubar, tearoff=0)
        self._selected_camera_mode = tk.IntVar()
        self._selected_camera_mode.set(0)
        self._mode_menu.add_radiobutton(
            label='Park assistant', 
            variable=self._selected_camera_mode, 
            value=0,
            command=self._enter_park_assistant_mode
        )
        self._mode_menu.add_radiobutton(
            label='Rearview mirror', 
            variable=self._selected_camera_mode, 
            value=1,
            command=self._enter_mirror_mode
        )
        self._mode_menu.add_radiobutton(
            label='Configuration', 
            variable=self._selected_camera_mode, 
            value=2,
            command=self._enter_config_mode
        )
        self._menubar.add_cascade(menu=self._mode_menu, label='Mode')
    
    def show(self) -> None:
        self._updateVideoFrame(self._video_source.process_next_frame())
        self._window.mainloop()
    
    def _updateVideoFrame(self, video_frame: MatLike):
        if video_frame is None or video_frame.shape[0] != self._display_size[0]\
           or video_frame.shape[1] != self._display_size[1]:
            video_frame = self._generate_placeholder_image()
        video_frame = ImageTk.PhotoImage(Image.fromarray(video_frame))
        self._display.photo_image = video_frame
        self._display.configure(image=video_frame)
        self._display.after(20, lambda frame=self._video_source.process_next_frame(): self._updateVideoFrame(frame))
    
    def select_video_file(self):
        return filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4")])
        
    def _generate_placeholder_image(self) -> MatLike:
        image = np.full(self._display_size, 0, dtype=np.uint8)
        image = cv.putText(
            img=image, 
            text='<NO VIDEO TO DISPLAY>', 
            org=(self._display_size[1]//4, self._display_size[0] // 2), 
            fontFace=cv.FONT_HERSHEY_PLAIN, 
            fontScale=2, 
            color=(255, 255, 255), 
            thickness=1
        )
        return image
