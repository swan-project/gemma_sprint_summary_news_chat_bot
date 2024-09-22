import flet as ft
from components.input_section import InputSection
from components.output_section import OutputSection
from components.list_view import ListView
from components.item import Item
from components.app_bar import AppBar

class InputOutputView(ft.UserControl):
    def __init__(self, pipe_finetuned):
        super().__init__()
        self.input_section = InputSection(pipe_finetuned, self.summarize_to_output)
        self.output_section = OutputSection(self.save_texts)
        self.list_view = ListView(self.on_item_click)
        self.app_bar = AppBar(self.reset)

    def on_item_click(self, item: Item):
        self.input_section.set_input_text(item.input)
        self.output_section.set_output_text(item.output)
        self.output_section.set_title(item.title)
        self.update()

    def summarize_to_output(self, text: str):
        self.input_section.update_prefix()
        self.output_section.set_output_text(text)

    def save_texts(self, e):
        input_text = self.input_section.get_input_text()
        self.output_section.save_to_local_storage(input_text)
        self.list_view.load_items()
        self.list_view.update()
    
    def reset(self, e):
        self.input_section.reset()
        self.output_section.reset()
        self.list_view.reset(e)

    def build(self):
        return ft.Column(
            controls=[
                self.app_bar,
                ft.Row(
                    controls=[
                        self.input_section,
                        self.output_section,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    spacing=30
                ),
                self.list_view
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=50
        )