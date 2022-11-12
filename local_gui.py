#!/usr/bin/python3

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from PIL import Image
import pytesseract
import threading
import tkinter as tk
from tkinter import filedialog
from translate import Translator
from kivy.uix.textinput import TextInput


def transalt(self, lang):
    try:
        root = tk.Tk()
        root.withdraw()
        image_path = filedialog.askopenfilename()
    
        if lang == "English":
            read_language = "eng"
            translate_lang = "en"

        elif lang == "Greek":
            read_language = "ell"
            translate_lang = "el"

        row = pytesseract.image_to_string(Image.open(image_path), lang=read_language)
        transalator = Translator(from_lang=translate_lang, to_lang="ru")
        data = transalator.translate(row)
        self.set_data_label(data)


    except AttributeError:
        pass
# Here Function finish

KV = """
MyBL:
        
        orientation: "vertical"
        size_hint: (0.95, 0.95)
        pos_hint: {"center_x": 0.5, "center_y":0.5}
        
        Label:
                font_size: "15sp"
                multiline: True
                text_size: self.width*0.98, None
                size_hint_x: 1.0
                size_hint_y: None
                height: self.texture_size[1] + 15
                text: root.data_label
        Button:                
                text: "English Transalte"
                bold: True
                background_color:(1,0,1)
                size_hint: (1,0.5)
                on_press: root.selectphoto()
        Button:
                text: "Greek Transalte"
                bold: True
                background_color:(1,0,1)
                size_hint: (1,0.5)
                on_press: root.Greek()
        Button:
                text: "Russian Read"
                bold: True
                background_color:(1,0,1)
                size_hint: (1,0.5)
                on_press: root.read()
"""

class MyBL(BoxLayout):
    data_label = StringProperty("PyTeleTransl Gui")
    
    def selectphoto(self):
        transalt(self, "English")

    def Greek(self):
        transalt(self, 'Greek')

    def read(self):
        try:
            root = tk.Tk()
            root.withdraw()
            image_path = filedialog.askopenfilename()
            data = pytesseract.image_to_string(Image.open(image_path), lang="rus")
            self.set_data_label(data)

        except AttributeError:
            pass
        
    def set_data_label(self, data):
        self.data_label += str(data) + "\n"

class MyApp(App):
    running = True

    def build(self):
        return Builder.load_string(KV)

    def on_stop(self):
        self.running = False

MyApp().run()
