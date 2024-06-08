"""
Moduł pośredniczący pomiędzy interfejsem graficznym, a modułami realizującymi 
logikę biznesową systemu. Odpowiadał on będzie za przechwytywanie zdarzeń 
przychodzących z interfejsu graficznego i wywołanie ich obsługi przy pomocy 
odpowiednich metod z pozostałych modułów (silnik przetwarzania obrazu 
lub odbiornik obrazu).  
"""
import asyncio
import time
from enum import Enum

import playsound

from backup_camera._image_processing.image_porcessor import ImageProcessingEngine
from backup_camera._image_receiver import ImageReceiver
from backup_camera._image_receiver import CAPTURE_VIDEO_FILE, NO_VIDEO_CAPTURE
from backup_camera._image_processing.image_parameters import ImageParameters


class ApplicationMode(Enum):
    PARK_ASSISTANT = 0
    REARWIEV_MIRROR = 1
    CONFIGURATION = 2
    

class Application:
    MIN_TIME_BETWEEN_ALERTS_SECONDS = 0.5
    
    def __init__(self, display_size: tuple[int, int]) -> None:
        from backup_camera._user_interface.user_interface import UserInteface   # used here to avoid circural import
        
        self.application_mode = ApplicationMode.REARWIEV_MIRROR
        self._image_parameters = ImageParameters.load_from_file()
        self._image_receiver = ImageReceiver()
        self._image_processor = ImageProcessingEngine(display_size, self._image_receiver, self._image_parameters, self)
        self._ui = UserInteface(display_size, self, self._image_processor)
        self._muted = False
        self._last_alert_time = None

    def get_config(self) -> dict[str]:
        return vars(self._image_parameters)

    def run(self):
        self._ui.show()
        self._image_receiver.end_capture()
        self._image_parameters.save_to_file()
    
    def set_image_properties(self, brightness, contrast, saturation):
        self._image_parameters.brightness = brightness
        self._image_parameters.contrast = contrast
        self._image_parameters.saturation = saturation
        
    def set_guidelines_properties(self, number_of_lines, x_offset, y_offset, spacing, tilt, y_line_height):
        self._image_parameters.number_of_lines = number_of_lines
        self._image_parameters.x_offset = x_offset
        self._image_parameters.y_offset = y_offset
        self._image_parameters.spacing = spacing
        self._image_parameters.tilt = tilt
        self._image_parameters.y_line_height = y_line_height

    def set_detection_properties(self, detect_cars, detect_bicycles, detect_pedestrians):
        self._image_parameters.detect_cars = detect_cars
        self._image_parameters.detect_bicycles = detect_bicycles
        self._image_parameters.detect_pedestrians = detect_pedestrians
    
    def set_guidelines_visibility(self, guidelines_hidden):
        self._image_parameters.guidelines_hidden = guidelines_hidden
    
    def change_mute_sounds(self):
        self._ui.mute()
        self._muted = not self._muted
    
    def set_source(self, source_id: int):
        if source_id >= 0:
            self._image_receiver.start_capture(source_id)
        elif source_id == CAPTURE_VIDEO_FILE:
            filename = self._ui.select_video_file()
            if filename == '' or filename == ():
                self._image_receiver.end_capture()
            else:
                self._image_receiver.start_capture(filename)
        elif source_id == NO_VIDEO_CAPTURE:
            self._image_receiver.end_capture()
    
    def play_alert(self) -> None:
        if self._muted or (self._last_alert_time is not None and\
           time.time() - self._last_alert_time < Application.MIN_TIME_BETWEEN_ALERTS_SECONDS):
            return
        self._last_alert_time = time.time()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._play_sound('alert.wav'))

    async def _play_sound(self, sound_file: str) -> None:
        playsound.playsound(sound_file)