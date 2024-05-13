from cv2.typing import MatLike

from backup_camera._image_processing._classifier import Classifier
from backup_camera._image_processing._preprocessor import Preprocessor
from backup_camera._image_processing._postprocessor import Postprocessor
from backup_camera._image_receiver import ImageReceiver
from backup_camera._image_processing.image_parameters import ImageParameters


class ImageProcessingEngine:
    def __init__(self, image_size: tuple[int, int], image_receiver: ImageReceiver, 
                 image_parameters: ImageParameters, parent_app) -> None:
        assert image_receiver != None, 'image receiver should not be None!'

        self.image_parameters = image_parameters
        self._image_size = image_size
        self._parent_app = parent_app

        self._image_receiver = image_receiver
        self._preprocessor = Preprocessor()
        self._classifier = Classifier()
        self._postprocessor = Postprocessor()
    
    def process_next_frame(self) -> MatLike|None:
        frame = self._image_receiver.get_frame()
        ui_frame, classifier_frame = self._preprocessor.preprocess(
            frame, self.image_parameters,
            self._parent_app.application_mode
        )
        detection_metadata = self._classifier.detect_objects(classifier_frame, self.image_parameters)
        return self._postprocessor.postprocess(ui_frame, detection_metadata, self._image_size)
    