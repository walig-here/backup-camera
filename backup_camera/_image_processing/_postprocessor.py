"""
Na podstawie kopii obrazu z kamery, przystosowanej do wyświetlania oraz 
metadanych otrzymanych z klasyfikatora przygotowuje ostateczną wersję obrazu, 
która zostanie zaprezentowana na interfejsie graficznym. Zakłada to nakładanie 
na obraz dodatkowych napisów, linii pomocniczych, ikon ostrzegawczych czy 
obramowań zawierających rozpoznane obiekty. Wytworzoną przez siebie wersję 
obrazu przesyła do interfejsu graficznego. 
"""
import math

import cv2 as cv
import numpy as np
from cv2.typing import MatLike

from backup_camera._image_processing.image_parameters import ImageParameters, MAX_X_OFFSET, MAX_Y_OFFSET, MAX_SPACING
from backup_camera._image_processing._classifier import DetectedObject, DetectableObjectType


class Postprocessor:
    _LINES_COLOR = (24, 202, 247)
    _CAR_BOUNDING_BOX_COLOR = (255, 0, 0)
    _PEDESTRIAN_BOUNDING_BOX_COLOR = (0, 255, 0)
    _CYCLIST_BOUNDING_BOX_COLOR = (0, 0, 255)
    
    def postprocess(self, frame: MatLike|None, detection_metadata,
                    image_parameters: ImageParameters, application_mode) -> MatLike|None:
        if frame is None:
            return None
        frame = self._draw_guidelines(frame, image_parameters, application_mode)
        frame = self._draw_bounding_boxes(frame, detection_metadata)
        return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    def _draw_guidelines(self, frame, image_parameters, application_mode):
        from backup_camera.application import ApplicationMode # added here to avoid circural import
        
        if not image_parameters.guidelines_hidden and \
                image_parameters.number_of_lines > 0 and \
                application_mode != ApplicationMode.REARWIEV_MIRROR:
                    self._apply_lines(frame, image_parameters)
        return frame
    
    def _draw_bounding_boxes(self, frame, detection_metatada: list[DetectedObject]):
        for detected_object in detection_metatada:
            frame = cv.rectangle(
                frame, 
                (detected_object.x, detected_object.y, detected_object.width, detected_object.height), 
                Postprocessor.get_bounding_box_color_for_object_type(detected_object.type),
                6
            )
        return frame

    @classmethod
    def get_bounding_box_color_for_object_type(cls, object: DetectableObjectType):
        match object:
            case DetectableObjectType.CAR: 
                return cls._CAR_BOUNDING_BOX_COLOR
            case DetectableObjectType.PEDESTRIAN:
                return cls._PEDESTRIAN_BOUNDING_BOX_COLOR
            case DetectableObjectType.CYCLIST:
                return cls._CYCLIST_BOUNDING_BOX_COLOR
            case _:
                return (255, 255, 255)
 
    def _apply_lines(self, frame, image_parameters: ImageParameters):
        width, height = frame.shape[1], frame.shape[0]
        single_line_height = int(0.11 * height)
        line_thickness = int(0.01 * width)
        lines_width = int(0.6 * width)
        horizontal_line = int(lines_width * 0.05)
        
        x_center = width // 2
        x_left = x_center - lines_width // 2
        x_right = x_center + lines_width // 2

        single_line_angle = int((x_center - x_left) / 2 * 0.25)

        first_y = height - single_line_height
        second_y = first_y - single_line_height
        third_y = second_y - single_line_height
        

        # CALCULATING HOW 1 on Y OFFSET SLIDER CORRESPONDS TO HEIGHT CHANGE:
        height_remaining = height - image_parameters.number_of_lines * single_line_height
            
        height_change = height_remaining * image_parameters.y_offset // MAX_Y_OFFSET
        # ------------------------------------------------------------------

        # CALUCLATING SPACING BETWEEN LINES:
        spacing = x_left * image_parameters.spacing // MAX_SPACING

        x_left = max(x_left - spacing, 0)
        x_right = min(x_right + spacing, width - 1)       
        # ------------------------------------------------------------------

        # # CALCULATING HOW 1 on X OFFSET SLIDER CORRESPONDS TO HEIGHT CHANGE:
        width_remaining = x_left

        width_change = width_remaining * image_parameters.x_offset // MAX_X_OFFSET
        # ------------------------------------------------------------------

        point1 = (x_left + width_change, height - height_change)
        point2 = (x_left + single_line_angle + width_change, first_y+1 - height_change)
        self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

        point1 = (x_right + width_change, height - height_change)
        point2 = (x_right - single_line_angle + width_change, first_y+1 - height_change)
        self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)
        
        y_coordinate = first_y + int(math.ceil(line_thickness/2)) + 1
        x_left = x_left + single_line_angle
        x_right = x_right - single_line_angle
        point1 = (x_left + width_change, y_coordinate - height_change)
        point2 = (x_left + horizontal_line + width_change, y_coordinate - height_change)
        self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

        point1 = (x_right + width_change, y_coordinate - height_change)
        point2 = (x_right - horizontal_line + width_change, y_coordinate - height_change)
        self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

        if image_parameters.number_of_lines > 1: # if number of lines = 2 or 3:
            point1 = (x_left + width_change, first_y - height_change)
            point2 = (x_left + single_line_angle + width_change, second_y+1 - height_change)
            self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

            point1 = (x_right + width_change, first_y - height_change)
            point2 = (x_right - single_line_angle + width_change, second_y+1 - height_change)
            self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

            y_coordinate = second_y + int(math.ceil(line_thickness/2)) + 1
            x_left = x_left + single_line_angle
            x_right = x_right - single_line_angle
            point1 = (x_left + width_change, y_coordinate - height_change)
            point2 = (x_left + horizontal_line + width_change, y_coordinate - height_change)
            self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

            point1 = (x_right + width_change, y_coordinate - height_change)
            point2 = (x_right - horizontal_line + width_change, y_coordinate - height_change)
            self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

        if image_parameters.number_of_lines == 3: # if number of lines = 3:
            point1 = (x_left + width_change, second_y - height_change)
            point2 = (x_left + single_line_angle + width_change, third_y+1 - height_change)
            self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

            point1 = (x_right + width_change, second_y - height_change)
            point2 = (x_right - single_line_angle + width_change, third_y+1 - height_change)
            self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

            y_coordinate = third_y + int(math.ceil(line_thickness/2)) + 1
            x_left = x_left + single_line_angle
            x_right = x_right - single_line_angle
            point1 = (x_left + width_change, y_coordinate - height_change)
            point2 = (x_left + horizontal_line + width_change, y_coordinate - height_change)
            self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)

            point1 = (x_right + width_change, y_coordinate - height_change)
            point2 = (x_right - horizontal_line + width_change, y_coordinate - height_change)
            self._draw_line(frame, point1, point2, self._LINES_COLOR, line_thickness)


    
    def _draw_line(self, img, pt1, pt2, color, thickness):
        x1, y1, x2, y2 = *pt1, *pt2
        theta = math.pi - np.arctan2(y1 - y2, x1 - x2)
        dx = int(math.sin(theta) * thickness / 2)
        dy = int(math.cos(theta) * thickness / 2)
        pts = [
            [x1 + dx, y1 + dy],
            [x1 - dx, y1 - dy],
            [x2 - dx, y2 - dy],
            [x2 + dx, y2 + dy]
        ]
        cv.fillPoly(img, [np.array(pts)], color)