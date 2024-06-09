"""
Dokonuje analizy obrazu i rozpoznania znajdujących się na nim obiektów 
przy pomocy metod uczenia maszynowego i sztucznej inteligencji (zakładane 
jest użycie klasyfikatora typu Haar Cascades). Efektem jego pracy powinny 
być metadane dotyczące rozpoznanych na obrazie obiektów. 
"""
import asyncio
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
    width: int
    height: int


class _ObjectDetector:
    def __init__(self, detected_object_type: DetectableObjectType, dataset_path: str, scale_factor: float, 
                 minium_neighbours: int, minimum_size_pixels: tuple[int, int], 
                 maximum_size_pixels: tuple[int, int]) -> None:
        self._classifier = cv.CascadeClassifier('datasets/' + dataset_path)
        self._detected_object_type = detected_object_type
        self._scale_factor = scale_factor
        self._minimum_neighbours = minium_neighbours
        self._minimum_size_pixels = [*minimum_size_pixels]
        self._maximum_size_pixels = [*maximum_size_pixels]
    
    async def detect_object_on_frame(self, frame) -> list[DetectedObject]:
        detection_results = self._classifier.detectMultiScale(
            image=frame,
            scaleFactor=self._scale_factor,
            minNeighbors=self._minimum_neighbours,
            minSize=self._minimum_size_pixels,
            maxSize=self._maximum_size_pixels
        )
        
        detected_objects = []
        for result in detection_results:
            detected_objects.append(DetectedObject(
                type=self._detected_object_type,
                x=result[0],
                y=result[1],
                width=result[2],
                height=result[3]
            ))
        return detected_objects
    

class Classifier:
    
    def __init__(self) -> None:
        self._cars_detector = _ObjectDetector(
            detected_object_type=DetectableObjectType.CAR,
            dataset_path='cars-4.xml',
            scale_factor=1.05,
            minium_neighbours=4,
            minimum_size_pixels=(100, 100),
            maximum_size_pixels=(600, 600)
        )
        self._cyclist_detector = _ObjectDetector(
            detected_object_type=DetectableObjectType.CYCLIST,
            dataset_path='haarcascade_russian_plate_number.xml',
            scale_factor=1.05,
            minium_neighbours=1,
            minimum_size_pixels=(30, 30),
            maximum_size_pixels=(200, 200)
        )
        self._pedestrians_detector = _ObjectDetector(
            detected_object_type=DetectableObjectType.PEDESTRIAN,
            dataset_path='haarcascade_fullbody.xml',
            scale_factor=1.06,
            minium_neighbours=6,
            minimum_size_pixels=(50, 150),
            maximum_size_pixels=(300, 900)
        )
    
    async def detect_object_async(self, frame: MatLike|None, image_parameters: ImageParameters, 
                                  application_mode) -> list[DetectedObject]:
        from backup_camera.application import ApplicationMode # added here to avoid circural import
        
        detected_objects = []
        tasks = []
        
        if application_mode in [ApplicationMode.REARWIEV_MIRROR, ApplicationMode.CONFIGURATION]\
           and image_parameters.detect_cars:
            tasks.append(self._cars_detector.detect_object_on_frame(frame.copy()))
        if application_mode in [ApplicationMode.REARWIEV_MIRROR, ApplicationMode.CONFIGURATION]\
           and image_parameters.detect_bicycles:
            tasks.append(self._cyclist_detector.detect_object_on_frame(frame.copy()))
        if application_mode in [ApplicationMode.PARK_ASSISTANT, ApplicationMode.CONFIGURATION]\
           and image_parameters.detect_pedestrians:
            tasks.append(self._pedestrians_detector.detect_object_on_frame(frame.copy()))
        results = await asyncio.gather(*tasks)
            
        for result in results:
            detected_objects.extend(result)
                
        return detected_objects
    
    def detect_objects(self, frame: MatLike|None, image_parameters: ImageParameters, 
                       application_mode) -> list[DetectedObject]:
        if frame is None:
            return []
        grayscale_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        grayscale_frame = cv.equalizeHist(grayscale_frame)
        grayscale_frame = cv.GaussianBlur(grayscale_frame, (5,5), 0)
        return asyncio.run(self.detect_object_async(grayscale_frame, image_parameters, application_mode))
