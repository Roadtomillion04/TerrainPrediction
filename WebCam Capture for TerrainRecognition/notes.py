'''
Difference between self.ids and self.manager.current_screen.ids is

self.ids looks for parent class ids
As in capture() we changed the screen to image screen
self.manager.current_screen.ids looks for current screen class


To change the default button layout, import the button image and change
background_normal: filepath
background_press: filepath


It' always good to declare self.variable in class inside methods
so that we can access it from other methods in same class instead returning
as well as other outside class


To access the variable of other screen use
App. get_running_app().root.ids.(id_name of that screen declared) in (root widget.variable name)
variable name should be self.variable


Label widget in kivy are not selectable in app

Use Window.clearcolor = (R, G, B, A) in build() to change background of kivy app


Use Clipboard.copy(str) to copy in our computer clipboard
'''

