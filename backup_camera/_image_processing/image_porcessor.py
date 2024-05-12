from cv2.typing import MatLike

from backup_camera._image_processing._classifier import Classifier
from backup_camera._image_processing._preprocessor import Preprocessor
from backup_camera._image_processing._postprocessor import Postprocessor
from backup_camera._image_receiver import ImageReceiver


class ImageProcessingEngine:
    def __init__(self, image_size: tuple[int, int], image_receiver: ImageReceiver) -> None:
        assert image_receiver != None, 'image receiver should not be None!'
        
        self._image_size = image_size

        self._image_receiver = image_receiver
        self._preprocessor = Preprocessor()
        self._classifier = Classifier()
        self._postprocessor = Postprocessor()
    
    def process_next_frame(self) -> MatLike|None:
        frame = self._image_receiver.get_frame()
        ui_frame, classifier_frame = self._preprocessor.preprocess(frame)
        detection_metadata = self._classifier.detect_objects(classifier_frame)
        return self._postprocessor.postprocess(ui_frame, detection_metadata, self._image_size)
        
    