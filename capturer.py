from threading import Thread
from cv2 import VideoCapture, imwrite
import pyautogui
import time
from utils import get_file_path


class Capturer:
    def __init__(
        self,
        photo_dir,
        screen_shot_dir
    ):
        self.photo_dir = photo_dir
        self.screen_shot_dir = screen_shot_dir
    
    def capture_status(self):
        photo_path = self.take_photo()
        screen_shot_path = self.screen_shot()
        return (photo_path, screen_shot_path)
    
    def take_photo(self) -> str:
        cap = VideoCapture(0)
        ret, frame = cap.read()
        file_path = get_file_path('jpg', 'photo', self.photo_dir)
        imwrite(file_path, frame)
        cap.release()
        return file_path
    
    def screen_shot(self) -> str:
        pic = pyautogui.screenshot()
        file_path = get_file_path('png', 'screenshot', self.screen_shot_dir)
        pic.save(file_path)
        return file_path


class Sleeper(Thread):
    def __init__(self, sleep_time, capturer, collector=None):
        super().__init__()
        self.sleep_time = sleep_time
        self.capturer = capturer
        self.collector = collector
    
    def run(self):
        while True:
            time.sleep(self.sleep_time)
            photo_path, screen_shot_path = self.capturer.capture_status()
            if self.collector is not None:
                response = self.collector.upload_file(photo_path, 'photo')
                response = self.collector.upload_file(screen_shot_path, 'screen_shot')
