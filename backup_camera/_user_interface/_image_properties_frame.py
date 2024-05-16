import tkinter as tk

from backup_camera.application import Application


class ImagePropertiesFrame(tk.Frame):
    def __init__(self, master, event_handler: Application) -> None:
        super().__init__(master, border=1)
        self._event_handler = event_handler
        
        self._label = tk.Label(self, text='Image Properties')
        self._label.pack()

        self._brightness = tk.Scale(
            self, from_=-100, to=100, orient=tk.HORIZONTAL, 
            variable=tk.IntVar(value=event_handler.get_config()['brightness']),
            label='Brightness',
            command=self._settings_changed
        )
        self._brightness.pack()

        self._contrast = tk.Scale(
            self, from_=-100, to=100, orient=tk.HORIZONTAL, 
            variable=tk.IntVar(value=event_handler.get_config()['contrast']),
            label='Contrast',
            command=self._settings_changed
        )
        self._contrast.pack()

        self._saturation = tk.Scale(
            self, from_=-100, to=100, orient=tk.HORIZONTAL, 
            variable=tk.IntVar(value=event_handler.get_config()['saturation']),
            label='Saturation',
            command=self._settings_changed
        )
        self._saturation.pack()
    
    def _settings_changed(self, _):
        self._event_handler.set_image_properties(
            brightness=self._brightness.get(),
            contrast=self._contrast.get(),
            saturation=self._saturation.get()
        )
        