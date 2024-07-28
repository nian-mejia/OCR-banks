import kivy
kivy.require('2.0.0')

import pyperclip

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

from kivy.graphics import Color, Rectangle


from ocr import main

info = ""

class MainScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 20
        self.padding = (20, 20)

        with self.canvas.before:
            # dibujar el rectángulo de fondo
            Color(1, 0.7, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(text="Selecciona el banco", font_size=40, bold=True, pos_hint = {'center_x': 0.5, 'center_y':0.7})
        self.add_widget(title_label)

        button_color = (0.5, 0, 0.5, 0.4)
        button_text_color = (1, 1, 1, 1)
        
        button_layout = RelativeLayout()
        rappi_button = Button(text="Rappi", size_hint=(None, None), size=(250, 100), background_color=button_color, color=button_text_color, 
                              pos_hint = {'center_x': 0.5, 'center_y':0.6})
        rappi_button.bind(on_press=self.on_button_press)
        button_layout.add_widget(rappi_button)

        banco1_button = Button(text="Bancolombia", size_hint=(None, None), size=(250, 100), background_color=button_color, color=button_text_color,
                               pos_hint = {'center_x': 0.5, 'center_y':0.5})
        banco1_button.bind(on_press=self.on_button_press)
        button_layout.add_widget(banco1_button)

        banco2_button = Button(text="Banco2", size_hint=(None, None), size=(250, 100), background_color=button_color, color=button_text_color,
                               pos_hint = {'center_x': 0.5, 'center_y':0.4})
        banco2_button.bind(on_press=self.on_button_press)
        button_layout.add_widget(banco2_button)

        self.add_widget(button_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        
        self.rect.size = instance.size
    def on_button_press(self, instance):
        global info
        button_text = instance.text
        info = main(button_text)
        self.clear_widgets()
        self.add_widget(TerminalScreen())

    


class TerminalScreen(BoxLayout):
    def __init__(self, **kwargs):
        global info
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.info = info

        message_input = Label(text=info, font_size=40, size_hint_y=None, height=600, halign='left')
        self.add_widget(message_input)

        copy_button = Button(text="Copiar todo")
        copy_button.bind(on_press=self.on_copy_button_press)
        self.add_widget(copy_button)

    def on_touch_move(self, touch):
        if touch.dx > 20:
            self.parent.clear_widgets()
            self.parent.add_widget(MainScreen())
            return True

    def on_copy_button_press(self, instance):
        pyperclip.copy(instance.parent.children[1].text)  # copiar el texto del TextInput

    def on_pre_enter(self):
        self.children[1].scroll_y = 1 

class MyApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
