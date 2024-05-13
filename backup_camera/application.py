"""
Moduł pośredniczący pomiędzy interfejsem graficznym, a modułami realizującymi 
logikę biznesową systemu. Odpowiadał on będzie za przechwytywanie zdarzeń 
przychodzących z interfejsu graficznego i wywołanie ich obsługi przy pomocy 
odpowiednich metod z pozostałych modułów (silnik przetwarzania obrazu 
lub odbiornik obrazu).  
"""
from enum import Enum

from backup_camera._image_processing.image_porcessor import ImageProcessingEngine
from backup_camera._image_receiver import ImageReceiver
from backup_camera._image_receiver import CAPTURE_VIDEO_FILE, NO_VIDEO_CAPTURE
from backup_camera._image_processing.image_parameters import ImageParameters


class ApplicationMode(Enum):
    REARWIEV_MIRROR = 0
    PARK_ASSISTANT = 1
    CONFIGURATION = 2
    

class Application:
    def __init__(self, display_size: tuple[int, int]) -> None:
        from backup_camera._user_interface.user_interface import UserInteface   # used here to avoid circural import
        
        self.application_mode = ApplicationMode.PARK_ASSISTANT
        self._image_parameters = ImageParameters()
        self._image_receiver = ImageReceiver()
        self._image_processor = ImageProcessingEngine(display_size, self._image_receiver, self._image_parameters)
        self._ui = UserInteface(display_size, self, self._image_processor)

    def run(self):
        self._ui.show()
        self._image_receiver.end_capture()
    
    def set_image_properties(self, brightness, contrast, saturation):
        #print(f'brightness={brightness}')                   # TODO need to be removed for release version
        #print(f'contrast={contrast}')
        #print(f'saturation={saturation}')
        
        self._image_parameters.brightness = brightness
        self._image_parameters.contrast = contrast
        self._image_parameters.saturation = saturation
        
    def set_guidelines_properties(self, number_of_lines, x_offset, y_offset, spacing):
        #print(f'number-of-lines={number_of_lines}')
        #print(f'x-offset={x_offset}')                       # TODO need to be removed for release version
        #print(f'y-offset={y_offset}')
        #print(f'spacing={spacing}')
        
        self._image_parameters.number_of_lines = number_of_lines
        self._image_parameters.x_offset = x_offset
        self._image_parameters.y_offset = y_offset
        self._image_parameters.spacing = spacing

    def set_detection_properties(self, detect_cars, detect_bicycles, detect_pedestrians):
        #print(f'detect-cars={detect_cars}')                 # TODO need to be removed for release version
        #print(f'detect-bicycles={detect_bicycles}')
        #print(f'detect-pedestrians={detect_pedestrians}')
        
        self._image_parameters.detect_cars = detect_cars
        self._image_parameters.detect_bicycles = detect_bicycles
        self._image_parameters.detect_pedestrians = detect_pedestrians
    
    def set_guidelines_visibility(self, guidelines_hidden):
        #print(f'guidelines-hidden={guidelines_hidden}')     # TODO need to be removed for release version
        
        self._image_parameters.guidelines_hidden = guidelines_hidden
    
    def change_mute_sounds(self):
        self._ui.mute()
    
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