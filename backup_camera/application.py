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
    PARK_ASSISTANT_MODE = 1
    RERVIEW_MIRROR_MODE = 2
    
    def __init__(self) -> None:
        from backup_camera._user_interface import UserInteface   # used here to avoid circural import
        
        self._image_receiver = ImageReceiver()
        self._image_processor = ImageProcessingEngine(self._image_receiver)
        self._ui = UserInteface(self, self._image_processor)
        
        self._camera_mode = Application.PARK_ASSISTANT_MODE
    
    def run(self):
        self._ui.show()
        self._image_receiver.end_capture()
    
    def set_image_properties(self):
        print('IMAGE PROPERTIES!')
        
    def set_guidelines_properties(self):
        print('GUIDELINES PROPERTIES!')
    
    def set_detection_properties(self):
        print('DETECTIOn PROPERTIES!')
    
    def set_source(self, source_index: int):
        if source_index >= 0:
            self._image_receiver.start_capture(source_index)
        elif source_index == -1:
            filename = self._ui.select_video_file()
            if filename == '':
                self._image_receiver.end_capture()
            else:
                self._image_receiver.start_capture(filename)
        else:
            self._image_receiver.end_capture()
    