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
from kivy.uix.textinput import TextInput
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyperclip


have_old_translte = False
driver = webdriver.Firefox()
driver.get("https://translate.google.com/")
element = driver.find_element(By.XPATH, """
/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button
""")
time.sleep(4) # If browser don't load all needest , he died

element.click()

translate_input = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea
        """)
select_language_input = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[5]/button/div[3]
        """)
select_language_input.click()

find_language = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[2]/div/div[2]/input
        """)
find_language.send_keys('Russian')
select_russian = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[2]/div/div[4]/div/div[1]
        """)
select_russian.click()

def transalt(self, lang):
    try:
        root = tk.Tk()
        root.withdraw()
        image_path = filedialog.askopenfilename()
    
        if lang == "English":
            read_language = "eng"

        elif lang == "Greek":
            read_language = "ell"

        row = pytesseract.image_to_string(Image.open(image_path), lang=read_language)
        global have_old_transalte

        if have_old_translte == False:
            transalt.send_keys(row)
            time.sleep(10)
            copy_answer = driver.find_element(By.XPATH, """
                /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[8]/div/div[4]/div[2]/div/span/button/div[3]
                """)
            copy_answer.click()
            answer = pyperclip.paste()
            
        self.set_data_label(answer)


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
