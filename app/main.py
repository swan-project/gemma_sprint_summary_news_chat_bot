import flet as ft
from components.input_output_view import InputOutputView
from modules.auth import authenticate

async def main(page: ft.Page):
    page.title = 'techsum'
    page.theme_mode = 'light'
    await authenticate()  # 비동기로 authenticate 호출
    page.add(InputOutputView())
    page.update()
        

ft.app(main)
