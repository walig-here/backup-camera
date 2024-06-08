"""
Na podstawie kopii obrazu z kamery, przystosowanej do wyświetlania oraz 
metadanych otrzymanych z klasyfikatora przygotowuje ostateczną wersję obrazu, 
która zostanie zaprezentowana na interfejsie graficznym. Zakłada to nakładanie 
na obraz dodatkowych napisów, linii pomocniczych, ikon ostrzegawczych czy 
obramowań zawierających rozpoznane obiekty. Wytworzoną przez siebie wersję 
obrazu przesyła do interfejsu graficznego. 
"""
from cv2.typing import MatLike
import cv2 as cv
import math
import numpy as np

from backup_camera._image_processing.image_parameters import ImageParameters, \
    MAX_X_OFFSET, MAX_Y_OFFSET, MAX_SPACING, MAX_TILT, MAX_Y_LINE_HEIGHT
from backup_camera._image_processing._classifier import DetectedObject


class Postprocessor:
    LINES_COLOR = (24, 202, 247)
    
    def postprocess(self, frame: MatLike|None, detection_metadata, image_size: tuple[int, int],
                    image_parameters: ImageParameters, application_mode) -> MatLike|None:
        if frame is None:
            return None
        frame = self._draw_bounding_boxes(frame, detection_metadata)
        frame = self._draw_guidelines(frame, image_parameters, application_mode)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return cv.resize(frame, image_size)


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
                (255),
                1
            )
        return frame


    def _apply_lines(self, frame, image_parameters: ImageParameters):
        width, height = frame.shape[1], frame.shape[0]
        
        single_line_height = int(0.08*height)
        remaining_height_for_3rd_line = height - single_line_height * 3
        y_line_height_add = remaining_height_for_3rd_line * image_parameters.y_line_height / MAX_Y_LINE_HEIGHT
        single_line_height = int(single_line_height + y_line_height_add / 3)

        line_thickness = int(width / 250)
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

        cv.line(frame, point1, point2, self.LINES_COLOR, line_thickness, lineType=cv.LINE_AA)
        return point1, point2
    

    def _draw_vertical_right_line_points(self, frame, line_thickness,
                                                x_right, vertical_line_up_limit, vertical_line_down_limit,
                                                width_change,
                                                height, height_change, single_line_angle):
        point1 = (x_right + width_change, vertical_line_down_limit - height_change)
        point2 = (x_right - single_line_angle + width_change, vertical_line_up_limit + 1 - height_change)

        cv.line(frame, point1, point2, self.LINES_COLOR, line_thickness, lineType=cv.LINE_AA)   
        return point1, point2                           


    def _draw_horizontal_left_line_points(self, frame, line_thickness, 
                                          x_left, y_coordinate, horizontal_line, width_change, height_change,):
        point1 = (x_left + width_change, y_coordinate - height_change)
        point2 = (x_left + horizontal_line + width_change, y_coordinate - height_change)

        cv.line(frame, point1, point2, self.LINES_COLOR, line_thickness, lineType=cv.LINE_AA)
        return point1, point2
    

    def _draw_horizontal_right_line_points(self, frame, line_thickness,
                                           x_right, y_coordinate, horizontal_line, width_change, height_change):
        point1 = (x_right + width_change, y_coordinate - height_change)
        point2 = (x_right - horizontal_line + width_change, y_coordinate - height_change)

        cv.line(frame, point1, point2, self.LINES_COLOR, line_thickness, lineType=cv.LINE_AA)
        return point1, point2


    def _adjust_x_coordinates_with_angle(self, x_left, x_right, single_line_angle):
        x_left = x_left + single_line_angle
        x_right = x_right - single_line_angle
        return x_left, x_right