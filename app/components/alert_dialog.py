import flet as ft
from typing import Callable, Optional

class AlertDialog(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.dialog = None
        self.page = None
    
    def open(self, page: ft.Page, title: str, content: str, btn_text: str, on_click: Optional[Callable[[], None]] = None):
        self.page = page
        
        if on_click is None:
            on_click = self.close
        
        self.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton(btn_text, on_click=on_click)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def close(self, e):
        self.dialog.open = False
        self.page.update()