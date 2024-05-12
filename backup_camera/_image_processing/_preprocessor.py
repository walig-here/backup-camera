"""
Podmoduł odbierający obraz z kamery i tworzący jego dwie wstępnie 
przetworzone kopie. Pierwsza z nich powinna być przystosowana do 
przeanalizowania przez klasyfikator, w celu rozpoznania znajdujących 
się na obrazie elementów. Druga powinna być przystosowana do prezentacji 
na interfejsie graficznym (zastosowanie efektów dot. jasności, kontrastu, 
saturacji itd.). 
"""
import numpy as np
import cv2 as cv
from cv2.typing import MatLike

class Preprocessor:
    def preprocess(self, frame: MatLike|None) -> tuple[MatLike|None, MatLike|None]:
        if frame is None:
            return (None, None)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return (self._preprocess_for_ui(frame), self._preprocess_for_classifier(frame))
    
    def _preprocess_for_ui(self, frame):
        frame = apply_saturation(frame, 0)
        frame = apply_brightness_contrast(frame, 0, 0)
        return frame
    
    def _preprocess_for_classifier(self, frame):
        return frame



def apply_saturation(frame: MatLike, saturation_value: int) -> MatLike:
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame[:,:,1] = np.clip(frame[:,:,1] + saturation_value, 0, 255)
    frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)

    return frame
    
    
def apply_brightness_contrast(frame, brightness=0.0, contrast=0.0):

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
            
        buf = cv.addWeighted(frame, alpha_b, frame, 0, gamma_b)
    else:
        buf = frame.copy()
        
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
            
        buf = cv.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf
    