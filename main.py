from backup_camera.application import Application
from backup_camera._image_processing._preprocessor import Preprocessor
import cv2 as cv

def main():
    scale = 1.3
    app = Application((int(1280 // scale), int(720 // scale)))
    app.run()
    
if __name__ == '__main__':
    main()
    