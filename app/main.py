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

import modules.config as config
# set develop or product mode.
config.set_config('product')  # 또는 set_config('product')

app = FastAPI(timeout=None)
if config.getENVMode() == "product":
    app.mount("/static", StaticFiles(directory="../app/assets"), name="static")

async def main(page: ft.Page):
    page.title = 'techsum'
    page.theme_mode = 'light'
    await authenticate()  
    pipe_finetuned = await load_models()
    page.add(InputOutputView(pipe_finetuned))
    page.update()       


# local program check

if config.getENVMode() == "product":
    flet_app = flet_fastapi.app(main,assets_dir='assets') 
    app.mount("/", flet_app)
else:
    ft.app(target=main, assets_dir="assets")

