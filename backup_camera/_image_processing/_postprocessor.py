"""
Na podstawie kopii obrazu z kamery, przystosowanej do wyświetlania oraz 
metadanych otrzymanych z klasyfikatora przygotowuje ostateczną wersję obrazu, 
która zostanie zaprezentowana na interfejsie graficznym. Zakłada to nakładanie 
na obraz dodatkowych napisów, linii pomocniczych, ikon ostrzegawczych czy 
obramowań zawierających rozpoznane obiekty. Wytworzoną przez siebie wersję 
obrazu przesyła do interfejsu graficznego. 
"""
from cv2.typing import MatLike
from cv2 import resize

class Postprocessor:
    def postprocess(self, frame: MatLike|None, detection_metadata) -> MatLike|None:
        if frame is None:
            return None
        return resize(frame, (1280, 720))
