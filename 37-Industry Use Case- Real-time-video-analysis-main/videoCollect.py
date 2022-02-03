import cv2
import base64
import json
import time
import kafkaUtil
import threading
import numpy as np
import globalVariables
import pafy

def __fetch_live_video(stream_addr, videoId, func):
    url = stream_addr
    video = pafy.new(url)
    best  = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(best.url)
    row = globalVariables.GLOBAL_ROW
    col = globalVariables.GLOBAL_COL
    interval = 1 / globalVariables.GLOBAL_FPS
    while True:
        time.sleep(interval)
        ret, frame = cap.read()
        if not ret:
            time.sleep(1)
            cap = cv2.VideoCapture(best.url)
            continue
        col = int(frame.shape[0] * row / frame.shape[1])
        frame = cv2.resize(frame, (row, col), interpolation=cv2.INTER_CUBIC)
        _, buffer = cv2.imencode('.jpg', frame)
        encodedJPG = base64.b64encode(buffer).decode('utf-8')
        t = int(round(time.time() * 1000))
        jsonObject = json.dumps({"videoId": videoId,
                                 "row": row,
                                 "col": col,
                                 "data": encodedJPG,
                                 "timestamp": t,
                                 "type": "jpg"})
        if callable(func):
            func(jsonObject)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

def collect(topic, videoId):
    producer = kafkaUtil.connect_kafka_producer()

    def func(json):
        kafkaUtil.publish_message(producer, topic, json)

    stream_addr = globalVariables.GLOBAL_STREAM_ADDRESS
    t = threading.Thread(target=__fetch_live_video, args=(stream_addr, videoId, func))
    t.start()
    print("Producing data")
