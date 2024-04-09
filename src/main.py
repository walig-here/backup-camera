import cv2 as cv


def main():
    video = cv.VideoCapture(0)
    is_running = True
    view_canny = False
    threshold_1 = 50
    threshold_2 = 150
    
    while is_running:
        isTrue, frame = video.read()
        if view_canny:
            frame = cv.Canny(frame, threshold_1, threshold_2)
        cv.imshow("Wideo", frame)
        
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            is_running = False
        elif key == ord('c'):
            view_canny = not view_canny
        elif key == ord('w') and view_canny:
            threshold_1 += 10
        elif key == ord('s') and view_canny:
            threshold_1 = threshold_1 - 10 if threshold_1 >= 10 else 0
            
    video.release()
    
if __name__ == '__main__':
    main()