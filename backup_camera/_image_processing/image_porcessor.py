import threading

from cv2.typing import MatLike

from backup_camera._image_processing._classifier import Classifier
from backup_camera._image_processing._preprocessor import Preprocessor
from backup_camera._image_processing._postprocessor import Postprocessor
from backup_camera._image_receiver import ImageReceiver
from backup_camera._image_processing.image_parameters import ImageParameters


class ImageProcessingEngine:
    def __init__(self, image_size: tuple[int, int], image_receiver: ImageReceiver, 
                 image_parameters: ImageParameters, parent_app) -> None:
        assert image_receiver is not None, 'image receiver should not be None!'

        self.image_parameters = image_parameters
        self._image_size = image_size
        self._parent_app = parent_app

        self._image_receiver = image_receiver
        self._preprocessor = Preprocessor()
        self._classifier = Classifier()
        self._postprocessor = Postprocessor()

    def process_next_frame(self) -> MatLike|None:
        frame = self._image_receiver.get_frame()
        frame = self._preprocessor.preprocess(frame, self.image_parameters, self._image_size)
        detection_metadata = self._classifier.detect_objects(frame, self.image_parameters, 
                                                             self._parent_app.application_mode)
        if len(detection_metadata) > 0:
            threading.Thread(target=self._parent_app.play_alert).start()
        return self._postprocessor.postprocess(frame, detection_metadata, self.image_parameters,  
                                               self._parent_app.application_mode)
