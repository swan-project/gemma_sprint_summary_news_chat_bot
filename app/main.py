import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import flet as ft
from components.input_output_view import InputOutputView
from modules.auth import authenticate
from modules.load_model import load_models

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import flet.fastapi as flet_fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI(timeout=None)
app.mount("/static", StaticFiles(directory="../app/assets"), name="static")

async def main(page: ft.Page):
    page.title = 'techsum'
    page.theme_mode = 'light'
    await authenticate()  # 비동기로 authenticate 호출
    pipe_finetuned = await load_models()
    page.add(InputOutputView(pipe_finetuned))
    page.update()       


# local program check
#ft.app(target=main, assets_dir="assets")

flet_app = flet_fastapi.app(main,assets_dir='assets') 
app.mount("/", flet_app)
