import flet as ft
from typing import Callable

class AppBar(ft.UserControl):
    def __init__(self, on_reset: Callable[[], None]):
        super().__init__()
        self.logo = ft.Image(
            src="/static/logo.svg",
            #src="logo.svg",
            fit=ft.ImageFit.CONTAIN,
            height=20,
        )
        self.title = ft.Text("techsum", size=24, weight=ft.FontWeight.BOLD)
        self.reset_button = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.REFRESH), 
                    ft.Text("reset"), 
                ],
                spacing=5,
            ),
            on_click=on_reset
        )

    def build(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    # self.title,
                    self.logo,
                    self.reset_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            border=ft.Border(bottom=ft.BorderSide(color="grey", width=1)),
            padding=5
        )