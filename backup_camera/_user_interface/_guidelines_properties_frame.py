import tkinter as tk
from tkinter import ttk

from backup_camera.application import Application
from backup_camera._image_processing.image_parameters import (
    DEFAULT_NUMBER_OF_LINES, MAX_SPACING, MAX_X_OFFSET, 
    MIN_SPACING, MAX_Y_OFFSET, MIN_X_OFFSET, MIN_Y_OFFSET,
    NUMBER_OF_LINES_OPTIONS)


class GuidelinesPropertiesFrame(tk.Frame):
    def __init__(self, master, event_handler: Application, guidelines_hidden: tk.BooleanVar) -> None:
        super().__init__(master, border=1)
        self._event_handler = event_handler
        
        self._label = tk.Label(self, text='Guidelines Properties')
        self._label.pack()
        
        self._guidelines_hidden = guidelines_hidden
        self._guidelines_hidden_checkbox = tk.Checkbutton(
            self, 
            variable=guidelines_hidden, 
            text='Guidelines hidden',
            command=self._guidelines_visibility_changes
        )
        self._guidelines_hidden_checkbox.pack()
        
        self._spacing = tk.Scale(
            self, from_=MIN_SPACING, to=MAX_SPACING, orient=tk.HORIZONTAL, 
            label='Spacing',
            command=self._settings_changed
        ) 
        self._spacing.pack()
        
        self._x_offset = tk.Scale(
            self, from_=MIN_X_OFFSET, to=MAX_X_OFFSET, orient=tk.HORIZONTAL, 
            label='Offset X',
            command=self._settings_changed
        ) 
        self._x_offset.pack()
        
        self._y_offset = tk.Scale(
            self, from_=MIN_Y_OFFSET, to=MAX_Y_OFFSET, orient=tk.HORIZONTAL, 
            label='Offset Y',
            command=self._settings_changed
        ) 
        self._y_offset.pack()
        
        self._lines = tk.IntVar()
        self._lines.set(DEFAULT_NUMBER_OF_LINES)
        self._number_of_lines_label = tk.Label(self, text='Number of lines')
        self._number_of_lines_label.pack()
        self._number_of_lines = ttk.Combobox(self, textvariable=self._lines)
        self._number_of_lines.bind('<<ComboboxSelected>>', self._number_of_lines_changed)
        self._number_of_lines.pack()
        self._number_of_lines['values'] = NUMBER_OF_LINES_OPTIONS
    
    def _number_of_lines_changed(self, _):
        self._settings_changed()
    
    def _guidelines_visibility_changes(self):
        self._event_handler.set_guidelines_visibility(self._guidelines_hidden.get())
    
    def _settings_changed(self, _ = ''):
        self._event_handler.set_guidelines_properties(
            x_offset=self._x_offset.get(),
            y_offset=self._y_offset.get(),
            spacing=self._spacing.get(),
            number_of_lines=int(self._number_of_lines.get())
        )
