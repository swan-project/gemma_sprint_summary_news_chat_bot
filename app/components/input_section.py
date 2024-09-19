import flet as ft
from typing import Callable

class InputSection(ft.UserControl):
    def __init__(self, on_summarize: Callable[[str], None]):
        super().__init__()
        self.text_field = ft.TextField(
            border_color=ft.colors.TRANSPARENT,
            value="https://www.sciencetimes.co.kr/",
            label="Input Text",
            multiline=True,
            width=400,
            height=400
        )

        # mode에 따라 탭을 추가
        self.mode = "link"  # 기본 모드는 link로 설정
        self.tabs = ft.Tabs(
            tabs=[
                ft.Tab(text="Link Mode"),
                ft.Tab(text="Text Mode")
            ],
            on_change=self.on_tab_change
        )

        self.on_summarize = on_summarize

    def get_input_text(self):
        return self.text_field.value

    def set_input_text(self, text: str):
        self.text_field.value = text
        self.update()

    def reset(self):
        self.mode = "link"
        self.update_prefix()

    # Tab을 전환할 때 호출되는 메서드
    def on_tab_change(self, e):
        selected_tab = self.tabs.tabs[self.tabs.selected_index].text
        self.mode = "link" if "Link" in selected_tab else "text"
        self.update_prefix()
        print(f"Selected mode: {self.mode}")
    
    def update_prefix(self):
        if self.mode == "link":
            self.text_field.value = "https://www.sciencetimes.co.kr/",
        else:
            self.text_field.value = ""
        self.update()

    def summarize(self, e):
        input_text = self.text_field.value
        if self.mode == "link":
            text_summary = f"{input_text}"
        else:
            text_summary = f"Summarized content in {self.mode} mode: {input_text}"
        self.on_summarize(text_summary)

    def build(self):
        return ft.Column(
            controls=[
                self.tabs,
                self.text_field,
                ft.Row(
                    controls=[
                        ft.ElevatedButton(text="Summarize to Output", on_click=self.summarize)
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            spacing=30
        )

