import cv2

FRAMERATE = 8

video_capture = cv2.VideoCapture("./vids/vid0_full.mp4")
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv2.VideoWriter("./vids/vid0.avi", fourcc, FRAMERATE, (1920, 1080))
video_capture.set(cv2.CAP_PROP_POS_FRAMES, FRAMERATE*47)
count = 0
while(True):
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if(frame is None):
        break  # check for empty frames
    # img_copy = utils.find_keypoints(frame)

    out.write(frame)
    cv2.imshow('Original', frame)  # show on window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Exit when Q is pressed
    count += 1
    if count == FRAMERATE * 80:
        break


# Release the camera

video_capture.release()
print("Bye...")
