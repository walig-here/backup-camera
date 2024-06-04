"""
Dokonuje analizy obrazu i rozpoznania znajdujących się na nim obiektów 
przy pomocy metod uczenia maszynowego i sztucznej inteligencji (zakładane 
jest użycie klasyfikatora typu Haar Cascades). Efektem jego pracy powinny 
być metadane dotyczące rozpoznanych na obrazie obiektów. 
"""
from dataclasses import dataclass
from enum import Enum

import cv2 as cv
from cv2.typing import MatLike, Rect

from backup_camera._image_processing.image_parameters import ImageParameters

class DetectableObjectType(Enum):
    CYCLIST = 0
    CAR = 1
    PEDESTRIAN = 2
    

@dataclass
class DetectedObject:
    type: DetectableObjectType
    x: int
    y: int
    x: int
    width: int
    height: int
    

class Classifier:
    SCALE_FACTOR = 1.05
    MINIMUM_NEIGHBORS = 2
    MINIMUM_SIZE_PIXELS = [30, 30]
    MAXIMUM_SIZE_PIXELS = [200, 200]
    
    def __init__(self) -> None:
        self._classifier = cv.CascadeClassifier('haarcascade_license_plate_rus_16stages.xml')
    
    def detect_objects(self, frame: MatLike|None, image_parameters: ImageParameters) -> list[DetectedObject]:
        if frame is None:
            return []
        
        detection_results = self._classifier.detectMultiScale(
            image=frame,
            scaleFactor=self.SCALE_FACTOR,
            minNeighbors=self.MINIMUM_NEIGHBORS,
            minSize=self.MINIMUM_SIZE_PIXELS,
            maxSize=self.MAXIMUM_SIZE_PIXELS
        )
        
        detected_objects = []
        for result in detection_results:
            detected_objects.append(DetectedObject(
                type=DetectableObjectType.CAR,
                x=result[0],
                y=result[1],
                width=result[2],
                height=result[3]
            ))
        return detected_objects
