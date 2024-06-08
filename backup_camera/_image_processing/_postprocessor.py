"""
Na podstawie kopii obrazu z kamery, przystosowanej do wyświetlania oraz 
metadanych otrzymanych z klasyfikatora przygotowuje ostateczną wersję obrazu, 
która zostanie zaprezentowana na interfejsie graficznym. Zakłada to nakładanie 
na obraz dodatkowych napisów, linii pomocniczych, ikon ostrzegawczych czy 
obramowań zawierających rozpoznane obiekty. Wytworzoną przez siebie wersję 
obrazu przesyła do interfejsu graficznego. 
"""
import math
import time

import cv2 as cv
import numpy as np
from cv2.typing import MatLike

from backup_camera._image_processing.image_parameters import ImageParameters, \
    MAX_X_OFFSET, MAX_Y_OFFSET, MAX_SPACING, MAX_TILT, MAX_Y_LINE_HEIGHT
from backup_camera._image_processing._classifier import DetectedObject, DetectableObjectType


class Postprocessor:
    _LINES_COLOR = (24, 202, 247)
    _CAR_BOUNDING_BOX_COLOR = (1, 168, 255)
    _PEDESTRIAN_BOUNDING_BOX_COLOR = (0, 0, 255)
    _CYCLIST_BOUNDING_BOX_COLOR = (0, 0, 255)
    _CAR_ICON = cv.imread('car.png', cv.IMREAD_UNCHANGED)
    _PEDESTRIAN_ICON = cv.imread('pedestrian.png', cv.IMREAD_UNCHANGED)
    _CYCLIST_ICON = cv.imread('cyclist.png', cv.IMREAD_UNCHANGED)
    
    def __init__(self):
        self._car_detected = False
        self._pedestrian_detected = False
        self._cyclist_detected = False
        self._icon_display_start_time_seconds = None
    
    def postprocess(self, frame: MatLike|None, detection_metadata,
                    image_parameters: ImageParameters, application_mode) -> MatLike|None:
        if frame is None:
            return None
        frame = self._draw_bounding_boxes_and_icons(frame, detection_metadata)
        frame = self._draw_guidelines(frame, image_parameters, application_mode)
        return cv.cvtColor(frame, cv.COLOR_BGR2RGB)


    def _draw_guidelines(self, frame, image_parameters, application_mode):
        from backup_camera.application import ApplicationMode # added here to avoid circural import
        
        if not image_parameters.guidelines_hidden and \
                image_parameters.number_of_lines > 0 and \
                application_mode != ApplicationMode.REARWIEV_MIRROR:
                    self._apply_lines(frame, image_parameters)
        return frame
    
    def _draw_bounding_boxes_and_icons(self, frame, detection_metatada: list[DetectedObject]):
        if self._icon_display_start_time_seconds is not None and \
           time.time() - self._icon_display_start_time_seconds > 1:
            self._car_detected = False
            self._pedestrian_detected = False
            self._cyclist_detected = False
        
        for detected_object in detection_metatada:
            frame = cv.rectangle(
                frame, 
                (detected_object.x, detected_object.y, detected_object.width, detected_object.height), 
                Postprocessor.get_bounding_box_color_for_object_type(detected_object.type),
                4
            )
            match detected_object.type:
                case DetectableObjectType.CAR:
                    self._car_detected = True
                    self._icon_display_start_time_seconds = time.time()
                case DetectableObjectType.PEDESTRIAN:
                    self._pedestrian_detected = True
                    self._icon_display_start_time_seconds = time.time()
                case DetectableObjectType.CYCLIST:
                    self._cyclist_detected = True
                    self._icon_display_start_time_seconds = time.time()
        
        if self._car_detected:
            frame = self._draw_icon(frame, DetectableObjectType.CAR)
        elif self._pedestrian_detected:
            frame = self._draw_icon(frame, DetectableObjectType.PEDESTRIAN)
        elif self._cyclist_detected:
            frame = self._draw_icon(frame, DetectableObjectType.CYCLIST)
            
        return frame

    def _draw_icon(self, frame: MatLike, detected_object_type: DetectableObjectType):
        match detected_object_type:
            case DetectableObjectType.CAR:
                current_icon = Postprocessor._CAR_ICON
                icon_width = current_icon.shape[1]
                icon_height = current_icon.shape[0]
                icon_x = frame.shape[1] // 2 - icon_width // 2
                icon_y = frame.shape[0] - 10 - icon_height
            case DetectableObjectType.PEDESTRIAN:
                current_icon = Postprocessor._PEDESTRIAN_ICON
                icon_width = current_icon.shape[1]
                icon_height = current_icon.shape[0]
                icon_x = frame.shape[1] // 2 - icon_width // 2
                icon_y = frame.shape[0] - 10 - icon_height
            case DetectableObjectType.CYCLIST:
                current_icon = Postprocessor._CYCLIST_ICON
                icon_width = current_icon.shape[1]
                icon_height = current_icon.shape[0]
                icon_x = frame.shape[1] // 2 - icon_width // 2
                icon_y = frame.shape[0] - 10 - icon_height
            case _:
                return frame
        
        for x in range(icon_width):
            for y in range(icon_height):
                if current_icon[y,x,3] == 0.0:
                    continue
                frame[icon_y+y, icon_x+x] = current_icon[y,x,:3]
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
        
        single_line_height = int(0.08*height)
        remaining_height_for_3rd_line = height - single_line_height * 3
        y_line_height_add = remaining_height_for_3rd_line * image_parameters.y_line_height / MAX_Y_LINE_HEIGHT
        single_line_height = int(single_line_height + y_line_height_add / 3)

        line_thickness = int(width / 100)
        lines_width = int(0.1 * width)
        horizontal_line = int(lines_width*0.25)
        
        x_center = width // 2
        x_left = x_center - lines_width // 2
        x_right = x_center + lines_width // 2

        single_line_angle = int((x_center - x_left) / 2 * image_parameters.tilt / (MAX_TILT / 6))

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

        vertical_line_up_limit = height - single_line_height
        vertical_line_down_limit = height

        for i in range(image_parameters.number_of_lines):
            if i + 1 > image_parameters.number_of_lines:
                break

            self._draw_vertical_left_line_points(frame, line_thickness, 
                                                 x_left, vertical_line_up_limit, vertical_line_down_limit,
                                                               width_change, height, height_change, single_line_angle)

            self._draw_vertical_right_line_points(frame, line_thickness, 
                                                  x_right, vertical_line_up_limit, vertical_line_down_limit,
                                                                width_change, height, height_change, single_line_angle)

            y_coordinate = vertical_line_up_limit + int(math.ceil(line_thickness/2)) + 1
            x_left, x_right = self._adjust_x_coordinates_with_angle(x_left, x_right, single_line_angle)

            self._draw_horizontal_left_line_points(frame, line_thickness, x_left, y_coordinate, 
                                                   horizontal_line, width_change, height_change)
        
            self._draw_horizontal_right_line_points(frame, line_thickness, x_right, y_coordinate, 
                                                    horizontal_line, width_change, height_change)
            
            vertical_line_up_limit -= single_line_height
            vertical_line_down_limit -= single_line_height
        

    def _draw_vertical_left_line_points(self, frame, line_thickness,
                                               x_left, vertical_line_up_limit, vertical_line_down_limit,
                                               width_change, 
                                               height, height_change, single_line_angle):
        point1 = (x_left + width_change, vertical_line_down_limit - height_change)
        point2 = (x_left + single_line_angle + width_change, vertical_line_up_limit + 1 - height_change)

        cv.line(frame, point1, point2, self._LINES_COLOR, line_thickness, lineType=cv.LINE_AA)
        return point1, point2
    

    def _draw_vertical_right_line_points(self, frame, line_thickness,
                                                x_right, vertical_line_up_limit, vertical_line_down_limit,
                                                width_change,
                                                height, height_change, single_line_angle):
        point1 = (x_right + width_change, vertical_line_down_limit - height_change)
        point2 = (x_right - single_line_angle + width_change, vertical_line_up_limit + 1 - height_change)

        cv.line(frame, point1, point2, self._LINES_COLOR, line_thickness, lineType=cv.LINE_AA)   
        return point1, point2                           


    def _draw_horizontal_left_line_points(self, frame, line_thickness, 
                                          x_left, y_coordinate, horizontal_line, width_change, height_change,):
        point1 = (x_left + width_change, y_coordinate - height_change)
        point2 = (x_left + horizontal_line + width_change, y_coordinate - height_change)

        cv.line(frame, point1, point2, self._LINES_COLOR, line_thickness, lineType=cv.LINE_AA)
        return point1, point2
    

    def _draw_horizontal_right_line_points(self, frame, line_thickness,
                                           x_right, y_coordinate, horizontal_line, width_change, height_change):
        point1 = (x_right + width_change, y_coordinate - height_change)
        point2 = (x_right - horizontal_line + width_change, y_coordinate - height_change)

        cv.line(frame, point1, point2, self._LINES_COLOR, line_thickness, lineType=cv.LINE_AA)
        return point1, point2


    def _adjust_x_coordinates_with_angle(self, x_left, x_right, single_line_angle):
        x_left = x_left + single_line_angle
        x_right = x_right - single_line_angle
        return x_left, x_right
