"""
Moduł pośredniczący pomiędzy interfejsem graficznym, a modułami realizującymi 
logikę biznesową systemu. Odpowiadał on będzie za przechwytywanie zdarzeń 
przychodzących z interfejsu graficznego i wywołanie ich obsługi przy pomocy 
odpowiednich metod z pozostałych modułów (silnik przetwarzania obrazu 
lub odbiornik obrazu).  
"""
from backup_camera._image_processing.image_porcessor import ImageProcessingEngine
from backup_camera._image_receiver import ImageReceiver

class Application:
    def __init__(self, display_size: tuple[int, int]) -> None:
        from backup_camera._user_interface.user_interface import UserInteface   # used here to avoid circural import
        
        self._image_receiver = ImageReceiver()
        self._image_processor = ImageProcessingEngine(display_size, self._image_receiver)
        self._ui = UserInteface(display_size, self, self._image_processor)
    
    def run(self):
        self._ui.show()
        self._image_receiver.end_capture()
    
    def set_image_properties(self, brightness, contrast, saturation):
        print(f'brightness={brightness}')
        print(f'contrast={contrast}')
        print(f'saturation={saturation}')
        
    def set_guidelines_properties(self, number_of_lines, x_offset, y_offset, spacing):
        print(f'number-of-lines={number_of_lines}')
        print(f'x-offset={x_offset}')
        print(f'y-offset={y_offset}')
        print(f'spacing={spacing}')
    
    def set_detection_properties(self, detect_cars, detect_bicycles, detect_pedestrians):
        print(f'detect-cars={detect_cars}')
        print(f'detect-bicycles={detect_bicycles}')
        print(f'detect-pedestrians={detect_pedestrians}')
    
    def set_guidelines_visibility(self, guidelines_hidden):
        print(f'guidelines-hidden={guidelines_hidden}')
    
    def change_mute_sounds(self):
        print('MUTE SOUNDS')
        self._ui.mute()
    
    def set_source(self, source_index: int):
        if source_index >= 0:
            self._image_receiver.start_capture(source_index)
        elif source_index == -1:
            filename = self._ui.select_video_file()
            if filename == '' or filename == ():
                self._image_receiver.end_capture()
            else:
                self._image_receiver.start_capture(filename)
        else:
            self._image_receiver.end_capture()
    