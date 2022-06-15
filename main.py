import cv2 as opcv
import requests
import threading
from time import sleep

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.core.window import Window


URL = 'your url'
IMG_NAME = "test.jpg"
NEXT_RECOGNITION_SEC = 9.8
SEND = True
ANGLE = 0

Window.clearcolor=(1,1,1,1)

class CamApp(App):

    def build(self):
        self.title_label = Label(text="Title", size_hint=(1,.1), font_size= 22, color='#000000',)
        self.web_cam = Image(size_hint=(1,.5))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.title_label)
        layout.add_widget(self.web_cam)

        self.capture = opcv.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0) # 33 == frame rate per second
        return layout

    def wait_N_seconds(self):
        print("wainting", NEXT_RECOGNITION_SEC, "seconds...")
        sleep(NEXT_RECOGNITION_SEC)

        global SEND
        SEND = True

    def send_face(self):
        print("sending img...")
        files = {"input_image" : open(IMG_NAME, "rb")}
        r = requests.post(URL , files=files)

        global ANGLE
        if r.ok:
            print(r.text)
        
        t2 = threading.Thread(target=self.wait_N_seconds)
        t2.start()

    def update(self, *args):
        ret, frame_resized = self.capture.read()

        global SEND
        if SEND:
            SEND = False
            t = threading.Thread(target=self.send_face)
            t.start()

        buf = opcv.flip(frame_resized, 0).tobytes()
        img_texture = Texture.create(size=(frame_resized.shape[1], frame_resized.shape[0]), colorfmt='bgr')
        img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.web_cam.texture = img_texture

if __name__ == '__main__':
    CamApp().run()
