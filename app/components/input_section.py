import flet as ft
import asyncio
from typing import Callable
from modules.summarize import summarize_text
from modules.generate_title import generate_title
from components.alert_dialog import AlertDialog
from constants.links import sciencetimes
from modules.web_scraper import extract_article

class InputSection(ft.UserControl):
    def __init__(self, pipe_finetuned, on_summarize: Callable[[str, str], None]):
        super().__init__()
        self.text_field = ft.TextField(
            border_color=ft.colors.GREEN_400,
            value=sciencetimes,
            label="Input Text",
            multiline=True,
            height=400,
            on_change=self.on_text_change
        )

        self.mode = "link"  
        self.tabs = ft.Tabs(
            tabs=[
                ft.Tab(text="Link Mode"),
                ft.Tab(text="Text Mode")
            ],
            on_change=self.on_tab_change,
        )
        self.button = ft.ElevatedButton(
                        text="Summarize to Output", 
                        on_click=self.summarize,
                    )

        self.on_summarize = on_summarize
        self.dialog = AlertDialog()
        self.pipe_finetuned = pipe_finetuned

    def get_input_text(self):
        return self.text_field.value

    def set_input_text(self, text: str):
        self.text_field.value = text
        self.update()

    def get_mode(self):
        return self.mode
    
    def update_mode(self, mode: str):
        self.mode = mode
        self.update_prefix()

        if mode == "link":
            self.tabs.selected_index = 0  
        else:
            self.tabs.selected_index = 1 

        self.update()

    def reset(self):
        if self.mode == "link":
            self.text_field.value = sciencetimes
        else:
            self.text_field.value = ""

    def validate_input(self):
        if not self.text_field.value.startswith(sciencetimes):
            self.dialog.open(
                self.page,
                title="경고", 
                content="사이언스타임즈 사이트에서 기사를 불러오지 않으면 진행할 수 없습니다.",
                btn_text="확인"
            )
            return False
        return True
        
    def update_prefix(self):
        if self.mode == "link":
            self.text_field.value = "https://www.sciencetimes.co.kr/"
        else:
            self.text_field.value = "\n\n\n\n\n\n\n\n"
        self.update()
    
    def on_tab_change(self, e):
        selected_tab = self.tabs.tabs[self.tabs.selected_index].text
        self.mode = "link" if "Link" in selected_tab else "text"
        self.update_prefix()
        print(f"Selected mode: {self.mode}")

    def on_text_change(self, e):
        # Check if the text field is empty and update the button state
        is_empty = not self.text_field.value.strip()
        self.button.disabled = is_empty
        self.update()  

    async def get_article(self):
        is_valid, title_news, paragraphs = extract_article(self.text_field.value)
        if is_valid:
                combined_text = "\n\n".join(paragraphs)
                title = title_news
        else:
            self.dialog.open(
                self.page,
                title="오류",
                content="view_content 클래스를 찾을 수 없습니다.",
                btn_text="확인"
            )
        self.update_mode("text")
        self.text_field.value = combined_text
        self.on_summarize(title, 'Loading...')
        self.update()
        return title, combined_text
        
    async def summarize(self, e):
        self.button.disabled = True  
        self.button.text = "Summarizing..."  
        self.update()  

        self.on_summarize("Loading...", 'Loading...')
        
        input_text = self.text_field.value
        if self.mode == "link":
            if self.validate_input():
                title, paragraphs = await self.get_article()
                text_summary = await summarize_text(paragraphs, self.pipe_finetuned)
        else:
            text_wo_enter = self.text_field.value.replace("\n", "")  
            if len(text_wo_enter) < 100:
                self.dialog.open(
                    self.page,
                    title="경고",
                    content="입력 텍스트는 최소 100자 이상이어야 합니다.",
                    btn_text="확인"
                )            
                self.button.disabled = False 
                self.button.text = "Summarize to Output"  
                self.update()                
            else:
                print("summarzing", input_text)
                title, text_summary = await asyncio.gather(
                    generate_title(input_text, self.pipe_finetuned),
                    summarize_text(input_text, self.pipe_finetuned)
                )

        self.on_summarize(title, text_summary)
        self.button.disabled = False 
        self.button.text = "Summarize to Output"  
        self.update() 

    def build(self):
        return ft.Column(
            controls=[
                self.tabs,
                self.text_field,
                ft.Row(
                    controls=[self.button],
                    alignment=ft.MainAxisAlignment.END
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            spacing=30
        )

