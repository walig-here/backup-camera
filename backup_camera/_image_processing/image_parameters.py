from dataclasses import dataclass


MAX_SPACING = 100
MIN_SPACING = 0
MAX_X_OFFSET = 100
MIN_X_OFFSET = -100
MAX_Y_OFFSET = 100
MIN_Y_OFFSET = 0
NUMBER_OF_LINES_OPTIONS = [1, 2, 3]
DEFAULT_NUMBER_OF_LINES = 3


@dataclass
class ImageParameters: 
    detect_cars: bool = True
    detect_bicycles: bool = True
    detect_pedestrians: bool = True
    brightness: int = 0
    contrast: int = 0
    saturation: int = 0
    guidelines_hidden: bool = False
    number_of_lines: int = DEFAULT_NUMBER_OF_LINES
    x_offset: int = 0
    y_offset: int = 0
    spacing: int = 0
