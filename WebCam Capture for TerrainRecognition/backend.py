from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window # for bg

from output_prediction import plot_figure
from filesharer import FileSharer
import time
import sys

# load_file() is a class method not instance one
Builder.load_file(filename= 'frontend.kv') # connects frontend to backend

class CameraScreen(Screen): # first screen
    def start_webcam(self):
        self.ids.camera.play = True
        # or we can call directly
        self.ids.camera_button.text = 'Stop Camera'

        # to revert texture == None, gets last frame
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop_webcam(self):
        self.ids.camera.play = False
        self.ids.camera_button.text = 'start camera'

        # stop currently displays last_frame, to remove that
        self.ids.camera.texture = None

    def capture(self):  # str from time
        """
        Captures a photo of last frame when button clicked, and save it as
        current time image in files
        """
        current_time = time.strftime('%Y-%m-%d-%H-%M-%S')
        self.file_path = f"files/{current_time}.png"
        self.ids.camera.export_to_png(filename= self.file_path)

        # Change screen to ImageScreen
        self.manager.current = 'image_screen' # name we declared in kivy
        # manager calls ScreenManager
        self.manager.current_screen.ids.image_display.source = self.file_path


class ImageScreen(Screen): # second screen

    def create_link(self):
        """
        Accesses the captured photo filepath, and uploads it to
        web and inserts the link to label widget
        """
        # To get access to the image filepath of CameraScreen class
        image_file = App.get_running_app().root.ids.camera_screen.file_path

        # uploading image to cloud
        file_sharer = FileSharer(filepath= image_file)
        self.url = file_sharer.upload()

    def test_webcam_image(self): # new date time on button click
        self.create_link()
        self.file_name = time.strftime('%Y-%m-%d-%H-%M-%S')
        plot_figure(webcam_image= True,
                    webcam_image_url= self.url,
                    prediction_image_name= self.file_name)
        self.make_screen_transition()

    def test_random_image(self): # new date time on button click
        self.file_name = time.strftime('%Y-%m-%d-%H-%M-%S')
        plot_figure(random_image= True,
                    prediction_image_name= self.file_name)
        self.make_screen_transition()

    def make_screen_transition(self):
        print("screen changed")
        self.manager.current = 'output_screen' # name declared in frontend
        # manager calls ScreenManager
        self.manager.current_screen.ids.output_image.source = rf"/Users/nirmalkumar/Desktop/4. WebCam Capture for TerrainPrediction/predicted_images/{self.file_name}.jpg"

class OutputScreen(Screen):
    def change_to_camera_screen(self):
        self.manager.current = 'camera_screen'

    def exit_app(self):
        sys.exit()


# Common convention to run kivy app window
class RootWidget(ScreenManager):
    pass # we can add any method in future when needed

class MainApp(App):
    def build(self):        # r    g   b    a
        Window.clearcolor = (0.5, 0.3, 0.5, 1)
        return RootWidget()

MainApp().run()

