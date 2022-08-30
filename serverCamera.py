import cv2
import mediapipe as mp
import time
import base64
import requests
import uuid
cap = cv2.VideoCapture(0)
pTime = 0

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.75)
def frame_to_base64(frame):
    return base64.b64encode(frame)
while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    # print(results)

    if results.detections:
        for id, detection in enumerate(results.detections):
            # mpDraw.draw_detection(img, detection)
            # print(id, detection)
            # print(detection.score)
            # print(detection.location_data.relative_bounding_box)
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(img, bbox, (255, 0, 255), 2)
            cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                        (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 255), 2)
            # if (detection.score[0] * 100) >= 80:
                # cv2.imwrite("C:/Users/RD98/Documents/GitHub/test/chane-file/demo/" + str(uuid.uuid4()) + ".jpg", img)
                # print(frame_to_base64(img))
                # response = requests.post("http://192.168.100.74:3100/api/find-addict-by-image/receive-file",data = {'data':frame_to_base64(img)})
                # print(response)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 255, 0), 2)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q"):  # độ trễ 1/1000s , nếu bấm q sẽ thoát
        break
cap.release()  # giải phóng camera
cv2.destroyAllWindows()  # thoát tất cả các cửa sổ