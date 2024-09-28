import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import flet as ft
from components.input_output_view import InputOutputView
from modules.auth import authenticate
from modules.load_model import load_models

async def main(page: ft.Page):
    page.title = 'techsum'
    page.theme_mode = 'light'
    await authenticate()  # 비동기로 authenticate 호출
    pipe_finetuned = await load_models()
    page.add(InputOutputView(pipe_finetuned))
    page.update()       

ft.app(target=main, assets_dir="assets")
