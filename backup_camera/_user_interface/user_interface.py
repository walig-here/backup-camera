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
from backup_camera.application import ApplicationMode
from backup_camera._image_processing.image_porcessor import ImageProcessingEngine
from backup_camera._image_receiver import ImageReceiver
from backup_camera._image_receiver import NO_VIDEO_CAPTURE
from backup_camera._user_interface._detection_properties_frame import DetectionPropertiesFrame
from backup_camera._user_interface._guidelines_properties_frame import GuidelinesPropertiesFrame
from backup_camera._user_interface._image_properties_frame import ImagePropertiesFrame


MILISECONDS_PER_FRAME = 20


class UserInteface:
    def __init__(self, display_size: tuple[int, int], parent_application: Application, 
                 video_source: ImageProcessingEngine) -> None:
        self._window = tk.Tk()
        self._window.title('Backup Camera')
        self._window.geometry(f'{display_size[0]}x{display_size[1]}')
        self._window.resizable(False, False)
        
        self._parent_application = parent_application
        self._video_source = video_source
        self._display_size = (display_size[1], display_size[0])
        self._guidelines_hidden = tk.BooleanVar(value=parent_application.get_config()['guidelines_hidden'])
        self._mute_sounds = tk.BooleanVar(value=False)
        
        self._menubar = tk.Menu(master=self._window)
        self._init_mode_menu(parent_application.application_mode)
        self._init_source_menu()
        self._window.config(menu=self._menubar)
        
        self._display = tk.Label(master=self._window)
        self._display.pack(fill=tk.BOTH)
        
        self._mode_label = tk.Label(self._window)
        self._mode_label.place(x=10, y=10)
        
        self._mute_label = tk.Label(self._window, text='MUTED')
        self._mute_label.pack_forget()
        
        self._image_properties_frame = ImagePropertiesFrame(master=self._window, event_handler=self._parent_application)
        self._guidelines_properties_frame = GuidelinesPropertiesFrame(
            self._window, 
            self._parent_application, 
            self._guidelines_hidden
        )
        self._detection_properties_frame = DetectionPropertiesFrame(
            self._window,
            self._parent_application,
            self._mute_sounds
        )
        self._enter_mirror_mode()
    
    def _enter_mirror_mode(self):
        self._reload_default_layout()
        self._mode_label.config(text='REARVIEW MIRROR')
        self._parent_application.application_mode = ApplicationMode.REARWIEV_MIRROR
    
    def _enter_park_assistant_mode(self):
        self._reload_default_layout()
        self._mode_label.config(text='PARK ASSISTANT')
        self._parent_application.application_mode = ApplicationMode.PARK_ASSISTANT
    
    def _enter_config_mode(self):
        self._reload_default_layout()
        self._mode_label.config(text='CONFIGURATION')
        self._parent_application.application_mode = ApplicationMode.CONFIGURATION
        
        self._config_menu = tk.Menu(master=self._menubar, tearoff=0)
        self._config_menu.add_command(
            label='Open image properties', 
            command=self._show_image_properties
        )
        self._config_menu.add_separator()
        self._config_menu.add_checkbutton(
            label='Guidlines hidden',
            variable=self._guidelines_hidden,
            command=self.change_guidelines_visibility
        )
        self._config_menu.add_command(
            label='Open guidelines properties', 
            command=self._show_guidelines_properties
        )
        self._config_menu.add_separator()
        self._config_menu.add_checkbutton(
            label='Mute alerts',
            variable=self._mute_sounds,
            command=self._parent_application.change_mute_sounds
        )
        self._config_menu.add_command(
            label='Open detection properties',
            command=self._show_detection_properties
        )
        self._menubar.add_cascade(menu=self._config_menu, label='Configuration')
    
    def _hide_properties_frame(self):
        if self._guidelines_properties_frame.winfo_viewable():
            self._guidelines_properties_frame.place_forget()
        elif self._image_properties_frame.winfo_viewable():
            self._image_properties_frame.place_forget()
        elif self._detection_properties_frame.winfo_viewable():
            self._detection_properties_frame.place_forget()
    
    def _reload_default_layout(self):
        if self._menubar.index('end') > 2:                      
            self._menubar.delete(self._menubar.index('end')) # delete configuration menu when not in configuration mode
        self._hide_properties_frame()
    
    def _show_image_properties(self):
        self._hide_properties_frame()
        self._image_properties_frame.place(x=10, y=40)
    
    def _show_guidelines_properties(self):
        self._hide_properties_frame()
        self._guidelines_properties_frame.place(x=10, y=40)
    
    def _show_detection_properties(self):
        self._hide_properties_frame()
        self._detection_properties_frame.place(x=10, y=40)
    
    def change_guidelines_visibility(self):
        self._parent_application.set_guidelines_visibility(self._guidelines_hidden.get())
    
    def _init_source_menu(self):
        self._source_menu = tk.Menu(master=self._menubar, tearoff=0)
        self._selected_video_source_id = tk.IntVar()
        
        sources = ImageReceiver.get_available_sources()
        for source_name in sources:
            self._source_menu.add_radiobutton(
                label=source_name, 
                variable=self._selected_video_source_id, 
                value=sources[source_name],
                command=lambda source_index=sources[source_name]: self._parent_application.set_source(source_index)
            )
            
        self._selected_video_source_id.set(NO_VIDEO_CAPTURE)
        self._menubar.add_cascade(menu=self._source_menu, label='Video source')
        
    def _init_mode_menu(self, application_mode: ApplicationMode):
        self._mode_menu = tk.Menu(master=self._menubar, tearoff=0)
        self._selected_camera_mode = tk.IntVar()
        self._selected_camera_mode.set(application_mode)
        self._mode_menu.add_radiobutton(
            label='Park assistant', 
            variable=self._selected_camera_mode, 
            value=ApplicationMode.PARK_ASSISTANT,
            command=self._enter_park_assistant_mode
        )
        self._mode_menu.add_radiobutton(
            label='Rearview mirror', 
            variable=self._selected_camera_mode, 
            value=ApplicationMode.REARWIEV_MIRROR,
            command=self._enter_mirror_mode
        )
        self._mode_menu.add_radiobutton(
            label='Configuration', 
            variable=self._selected_camera_mode, 
            value=ApplicationMode.CONFIGURATION,
            command=self._enter_config_mode
        )
        self._menubar.add_cascade(menu=self._mode_menu, label='Mode')
    
    def show(self) -> None:
        self._updateVideoFrame(self._video_source.process_next_frame())
        self._window.mainloop()
    
    def mute(self):
        if self._mute_sounds.get():
            self._mute_label.place(x=self._display_size[1] - 55, y=10)
        else:
            self._mute_label.place_forget()

    def _updateVideoFrame(self, video_frame: MatLike):
        if video_frame is None or video_frame.shape[0] != self._display_size[0]\
           or video_frame.shape[1] != self._display_size[1]:
            video_frame = self._generate_placeholder_image()
        
        video_frame = ImageTk.PhotoImage(Image.fromarray(video_frame))
        self._display.photo_image = video_frame
        self._display.configure(image=video_frame)
        self._display.after(
            MILISECONDS_PER_FRAME, 
            lambda frame=self._video_source.process_next_frame(): self._updateVideoFrame(frame)
        )
    
    def select_video_file(self):
        return filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4")])
        
    def _generate_placeholder_image(self) -> MatLike:
        image = np.zeros(self._display_size, dtype=np.uint8)
        image = cv.putText(
            img=image, 
            text='<NO VIDEO TO DISPLAY>', 
            org=(self._display_size[1] // 4, self._display_size[0] // 2), 
            fontFace=cv.FONT_HERSHEY_PLAIN, 
            fontScale=2, 
            color=(255, 255, 255), 
            thickness=1
        )
        return image
