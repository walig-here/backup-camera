"""
Moduł odpowiedzialny za odbiór obrazu ze wskazanej kamery i obsłużenie 
połączenia z nią. Możliwym będzie sprecyzowanie, z którego z urządzeń 
podłączonych do komputera ma on odbierać obraz. Jego istotną 
funkcjonalnością będzie również możliwość symulacji pobierania obrazu z 
kamery poprzez wczytanie pliku wideo. Pozwoli to na przeprowadzenie testów 
systemu na przygotowanych wcześniej nagraniach.
"""
import cv2 as cv
from cv2.typing import MatLike

class ImageReceiver:
    
    def __init__(self) -> None:
        self._video_capture = None
    
    def start_capture(self, source: str|int) -> None:
        self.end_capture()
        self._video_capture = cv.VideoCapture(source)
    
    def end_capture(self) -> None:
        if self._video_capture is None:
            return
        self._video_capture.release()
        self._video_capture = None
    
    def get_frame(self) -> MatLike|None:
        if self._video_capture is None:
            return None
        _, frame = self._video_capture.read()
        return frame
    
    @staticmethod
    def get_available_sources() -> dict[str, int]:
        available_sources = {
            'None': -2,
            'Video file': -1
        }
        for i in range(10):
            cap = cv.VideoCapture(i)
            if cap.isOpened():
                available_sources[f'Camera {i}'] = i
                cap.release()
        return available_sources
