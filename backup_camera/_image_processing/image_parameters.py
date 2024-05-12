class ImageParameters:
    def __init__(self,
                 detect_cars, detect_bicycles, detect_pedestrians,
                 brightness, contrast, saturation,
                 guidelines_hidden, number_of_lines, x_offset, y_offset, spacing
        ) -> None:
          
        self.detect_cars = detect_cars
        self.detect_bicycles = detect_bicycles
        self.detect_pedestrians = detect_pedestrians
        self.brightness = brightness
        self.contrast = contrast
        self.saturation = saturation
        self.guidelines_hidden = guidelines_hidden
        self.number_of_lines = number_of_lines
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.spacing = spacing
