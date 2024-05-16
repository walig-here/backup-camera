import tkinter as tk

from backup_camera.application import Application


class DetectionPropertiesFrame(tk.Frame):
    def __init__(self, master, event_handler: Application, mute_sounds: tk.BooleanVar) -> None:
        super().__init__(master, border=1)
        self._event_handler = event_handler
        
        self._label = tk.Label(self, text='Detection Properties')
        self._label.pack()
        
        self._mute_sounds = mute_sounds
        self._mute_sounds_checkbox = tk.Checkbutton(
            self, 
            variable=mute_sounds, 
            text='Mute alerts',
            command=event_handler.change_mute_sounds
        )
        self._mute_sounds_checkbox.pack()
        
        self._detect_cars = tk.BooleanVar(value=event_handler.get_config()['detect_cars'])
        self._detect_cars_checbox = tk.Checkbutton(
            self, 
            variable=self._detect_cars, 
            text='Detect cars',
            command=self._settings_changed
        )
        self._detect_cars_checbox.pack()
        
        self._detect_bicycles = tk.BooleanVar(value=event_handler.get_config()['detect_bicycles'])
        self._detect_bicycles_checkbox = tk.Checkbutton(
            self, 
            variable=self._detect_bicycles, 
            text='Detect bicycles',
            command=self._settings_changed
        )
        self._detect_bicycles_checkbox.pack()
        
        self._detect_pedestrians = tk.BooleanVar(value=event_handler.get_config()['detect_pedestrians'])
        self._detect_pedestrians_checkbox = tk.Checkbutton(
            self, 
            variable=self._detect_pedestrians, 
            text='Detect pedestrians',
            command=self._settings_changed
        )
        self._detect_pedestrians_checkbox.pack()
    
    def _settings_changed(self):
        self._event_handler.set_detection_properties(
            detect_bicycles=self._detect_bicycles.get(),
            detect_cars=self._detect_cars.get(),
            detect_pedestrians=self._detect_pedestrians.get()
        )
