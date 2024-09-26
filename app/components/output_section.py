import flet as ft
from typing import Callable
from components.item import Item
import json
import uuid

class OutputSection(ft.UserControl):
    def __init__(self, on_save: Callable[[], None]):
        super().__init__()
        self.title_field = ft.TextField(
            label="Title", 
            value="Text Summary",
            border=ft.InputBorder.UNDERLINE,
        )
        self.text_field = ft.TextField(
            border_color=ft.colors.TRANSPARENT,
            label="Output Text", 
            multiline=True, 
            height=400,
        )
        self.next_id = 1  # ID를 자동으로 증가시키기 위한 변수
        self.on_save = on_save

    # Output 텍스트 필드에 값을 설정하는 메서드
    def set_output_text(self, text: str):
        self.text_field.value = text
        self.update()

    # 텍스트 필드의 값을 반환하는 메서드
    def get_output_text(self):
        return self.text_field.value
    
    # 타이틀 필드에 값을 설정하는 메서드
    def set_title(self, title: str):
        self.title_field.value = title
        self.update()

    # 타이틀 필드의 값을 반환하는 메서드
    def get_title(self):
        return self.title_field.value
    
    def reset(self):
        self.title_field.value = "Text Summary",
        self.text_field.value = ""

    # 데이터를 로컬 스토리지에 저장하는 메서드
    def save_to_local_storage(self, mode: str, input_text: str):
        item = Item(
            id=str(uuid.uuid4()), 
            mode=mode,
            title=self.get_title(),
            input=input_text,
            output=self.get_output_text()
        )

        try:
            try:
                with open("local_storage.json", "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            data.append(item.to_dict())

            with open("local_storage.json", "w") as f:
                json.dump(data, f, indent=4)

            print(f"Saved item: {item.to_dict()}")
        except Exception as e:
            print(f"Error saving data: {e}")


    def build(self):
        return ft.Column(
            controls=[
                self.title_field,
                self.text_field,
                ft.ElevatedButton(text="Save Texts", on_click=self.on_save)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            spacing=30,
        )
