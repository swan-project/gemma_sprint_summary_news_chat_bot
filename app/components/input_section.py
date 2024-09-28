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
            border_color=ft.colors.TRANSPARENT,
            value=sciencetimes,
            label="Input Text",
            multiline=True,
            height=400,
            on_change=self.on_text_change
        )

        # mode에 따라 탭을 추가
        self.mode = "link"  # 기본 모드는 link로 설정
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

        # mode에 따라 탭 선택 변경
        if mode == "link":
            self.tabs.selected_index = 0  # Link Mode 탭 선택
        else:
            self.tabs.selected_index = 1  # Text Mode 탭 선택

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
            self.text_field.value = "http`s://www.sciencetimes.co.kr/"
            # 웹페이지 URL
            #url = "https://www.sciencetimes.co.kr/news/%eb%82%b4-%ec%a3%bc%eb%b3%80-%ec%83%9d%eb%ac%bc-%ec%86%8c%eb%a6%ac%eb%a1%9c-%ec%83%9d%eb%ac%bc%eb%8b%a4%ec%96%91%ec%84%b1-%ec%97%b0%ea%b5%ac%ed%95%9c%eb%8b%a4%ec%86%8c%eb%a6%ac/?cat=31"
        else:
            self.text_field.value = ""
        self.update()
    
     # Tab을 전환할 때 호출되는 메서드
    def on_tab_change(self, e):
        selected_tab = self.tabs.tabs[self.tabs.selected_index].text
        self.mode = "link" if "Link" in selected_tab else "text"
        self.update_prefix()
        print(f"Selected mode: {self.mode}")

    def on_text_change(self, e):
        # 텍스트 필드가 비어있는지 확인하고 버튼 상태 업데이트
        is_empty = not self.text_field.value.strip()
        self.button.disabled = is_empty
        self.update()  # UI 업데이트
        
    async def summarize(self, e):
        self.button.disabled = True  # 버튼 비활성화
        self.button.text = "Summarizing..."  # 버튼 텍스트 변경
        self.update()  # UI 업데이트

        self.on_summarize("Loading...", 'Loading...')
        
        input_text = self.text_field.value
        if self.mode == "link":
            if self.validate_input():
                is_valid, title_news, paragraphs = extract_article(self.text_field.value)
                if is_valid:
                    combined_text = "\n\n".join(paragraphs)
                    text_summary = await summarize_text(combined_text, self.pipe_finetuned)
                    title = title_news
                else:
                    self.dialog.open(
                        self.page,
                        title="오류",
                        content="view_content 클래스를 찾을 수 없습니다.",
                        btn_text="확인"
                    )
        else:
            print("summarzing", input_text)
            title, text_summary = await asyncio.gather(
                generate_title(input_text, self.pipe_finetuned),
                summarize_text(input_text, self.pipe_finetuned)
            )
        self.on_summarize(title, text_summary)
        self.button.disabled = False  # 버튼 비활성화
        self.button.text = "Summarize to Output"  # 버튼 텍스트 변경
        self.update()  # UI 업데이트

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

