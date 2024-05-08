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
    
    def set_image_properties(self):
        print('IMAGE PROPERTIES!')
        
    def set_guidelines_properties(self):
        print('GUIDELINES PROPERTIES!')
    
    def set_detection_properties(self):
        print('DETECTIOn PROPERTIES!')
    
    def set_source(self):
        print('SET SOURCE!')
    