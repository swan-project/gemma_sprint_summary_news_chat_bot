import flet as ft
# from components.item import Item
from components.input_output_view import InputOutputView


def main(page: ft.Page):
    page.title = 'techsum'
    page.theme_mode = 'light'


    page.add(InputOutputView())
    page.update()

ft.app(main)
