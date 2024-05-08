"""
Moduł odpowiedzialny za odbiór obrazu ze wskazanej kamery i obsłużenie 
połączenia z nią. Możliwym będzie sprecyzowanie, z którego z urządzeń 
podłączonych do komputera ma on odbierać obraz. Jego istotną 
funkcjonalnością będzie również możliwość symulacji pobierania obrazu z 
kamery poprzez wczytanie pliku wideo. Pozwoli to na przeprowadzenie testów 
systemu na przygotowanych wcześniej nagraniach.
"""
from cv2 import VideoCapture
from cv2.typing import MatLike

class ImageReceiver:
    def __init__(self) -> None:
        self._video_capture = None
    
    def start_capture(self, source: int|str) -> None:
        self._video_capture = VideoCapture(source)
    
    def get_frame(self) -> MatLike|None:
        if self._video_capture is None:
            return None
        _, frame = self._video_capture.read()
        return frame
