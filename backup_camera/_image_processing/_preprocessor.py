"""
Podmoduł odbierający obraz z kamery i tworzący jego dwie wstępnie 
przetworzone kopie. Pierwsza z nich powinna być przystosowana do 
przeanalizowania przez klasyfikator, w celu rozpoznania znajdujących 
się na obrazie elementów. Druga powinna być przystosowana do prezentacji 
na interfejsie graficznym (zastosowanie efektów dot. jasności, kontrastu, 
saturacji itd.). 
"""
import cv2 as cv
from cv2.typing import MatLike

class Preprocessor:
    def preprocess(self, frame: MatLike|None) -> tuple[MatLike|None, MatLike|None]:
        if frame is None:
            return (None, None)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return (self._preprocess_for_ui(frame), self._preprocess_for_classifier(frame))
    
    def _preprocess_for_ui(self, frame):
        return frame
    
    def _preprocess_for_classifier(self, frame):
        return frame
    