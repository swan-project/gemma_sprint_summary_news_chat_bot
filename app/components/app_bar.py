import flet as ft
from typing import Callable

class AppBar(ft.UserControl):
    def __init__(self, on_reset: Callable[[], None]):
        super().__init__()
        self.title = ft.Text("techsum", size=24, weight=ft.FontWeight.BOLD)
        self.reset_button = ft.IconButton(
            icon=ft.icons.REFRESH,
            on_click=on_reset
        )

    def build(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.title,
                    self.reset_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            border=ft.Border(bottom=ft.BorderSide(color="grey", width=1))
        )