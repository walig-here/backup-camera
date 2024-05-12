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
from backup_camera._image_processing.image_parameters import ImageParameters

class Preprocessor:
    yellow = (24, 202, 247)
    max_horizontal_lines = 3

    def preprocess(self, frame: MatLike|None, image_parameters: ImageParameters|None) -> tuple[MatLike|None, MatLike|None]:
        if frame is None:
            return (None, None)
        return (self._preprocess_for_ui(frame, image_parameters), self._preprocess_for_classifier(frame))
    
    def _preprocess_for_ui(self, frame, image_parameters):
        frame = self.apply_saturation(frame, image_parameters.saturation)
        frame = self.apply_brightness_contrast(frame, image_parameters.brightness, image_parameters.contrast)
        if not image_parameters.guidelines_hidden:
            self._draw_lines(frame)
        return frame
    
    def _preprocess_for_classifier(self, frame):
        return frame

    def apply_saturation(self, frame: MatLike, saturation_value: int) -> MatLike:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        frame[:,:,1] = np.clip(frame[:,:,1] + saturation_value, 0, 255)
        frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)

        return frame
        
    def apply_brightness_contrast(self, frame, brightness=0.0, contrast=0.0):
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
    
    def _draw_lines(self, frame):
        width, height = frame.shape[1], frame.shape[0]
        single_line_height = int(0.11 * height)
        line_thickness = int(0.01 * width)
        lines_width = int(0.60 * width)
        horizontal_line = int(lines_width * 0.05)
        
        x_center = width // 2
        x_left = x_center - lines_width // 2
        x_right = x_center + lines_width // 2

        single_line_angle = int((x_center - x_left) / 2 * 0.25)

        first_y = height - single_line_height
        second_y = first_y - single_line_height
        third_y = second_y - single_line_height
        print(first_y, second_y, third_y, height)

        self._draw_line(frame, (x_left, height), (x_left + single_line_angle, first_y+1), self.yellow, line_thickness)
        self._draw_line(frame, (x_right, height), (x_right - single_line_angle, first_y+1), self.yellow, line_thickness)
        y_coordinate = first_y + int(np.ceil(line_thickness/2)) + 1
        x_left = x_left + single_line_angle
        x_right = x_right - single_line_angle
        self._draw_line(frame, (x_left, y_coordinate),
                            (x_left + horizontal_line, y_coordinate),
                            self.yellow, line_thickness)
        self._draw_line(frame, (x_right, y_coordinate),
                            (x_right - horizontal_line, y_coordinate),
                            self.yellow, line_thickness)

        if True: # if number of lines > 1:
            self._draw_line(frame, (x_left, first_y), (x_left + single_line_angle, second_y+1), self.yellow, line_thickness)
            self._draw_line(frame, (x_right, first_y), (x_right - single_line_angle, second_y+1), self.yellow, line_thickness)
            y_coordinate = second_y + int(np.ceil(line_thickness/2)) + 1
            x_left = x_left + single_line_angle
            x_right = x_right - single_line_angle
            self._draw_line(frame, (x_left, y_coordinate),
                            (x_left + horizontal_line, y_coordinate),
                            self.yellow, line_thickness)
            self._draw_line(frame, (x_right, y_coordinate),
                            (x_right - horizontal_line, y_coordinate),
                            self.yellow, line_thickness)

        if True: # if number of lines > 2:
            self._draw_line(frame, (x_left, second_y), (x_left + single_line_angle, third_y+1), self.yellow, line_thickness)
            self._draw_line(frame, (x_right, second_y), (x_right - single_line_angle, third_y+1), self.yellow, line_thickness)
            y_coordinate = third_y + int(np.ceil(line_thickness/2)) + 1
            x_left = x_left + single_line_angle
            x_right = x_right - single_line_angle
            self._draw_line(frame, (x_left, y_coordinate),
                            (x_left + horizontal_line, y_coordinate),
                            self.yellow, line_thickness)
            self._draw_line(frame, (x_right, y_coordinate),
                            (x_right - horizontal_line, y_coordinate),
                            self.yellow, line_thickness)


    
    def _draw_line(self, img, pt1, pt2, color, thickness):
        x1, y1, x2, y2 = *pt1, *pt2
        theta = np.pi - np.arctan2(y1 - y2, x1 - x2)
        dx = int(np.sin(theta) * thickness / 2)
        dy = int(np.cos(theta) * thickness / 2)
        pts = [
            [x1 + dx, y1 + dy],
            [x1 - dx, y1 - dy],
            [x2 - dx, y2 - dy],
            [x2 + dx, y2 + dy]
        ]
        cv.fillPoly(img, [np.array(pts)], color)

        