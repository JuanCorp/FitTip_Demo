import asyncio
import os
import cv2
import base64





def extract_frames(video_path, frame_interval=20):
    """Extract every nth frame from a video."""
    video = cv2.VideoCapture(video_path)
    frames = []
    index = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        if index % frame_interval == 0:
            _, buffer = cv2.imencode(".jpg", frame)
            frames.append(base64.b64encode(buffer).decode("utf-8"))
        index += 1
    video.release()
    return frames



