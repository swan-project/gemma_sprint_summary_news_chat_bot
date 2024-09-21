import flet as ft
from typing import Callable
import requests
from bs4 import BeautifulSoup

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

    def validate_input(self):
        if not self.text_field.value.startswith("https://www.sciencetimes.co.kr"):
            # 경고 대화상자 생성
            dlg = ft.AlertDialog(
                title=ft.Text("경고"),
                content=ft.Text("사이언스타임즈 사이트에서 기사를 불러오지 않으면 진행할 수 없습니다."),
                actions=[
                    ft.TextButton("확인", on_click=self.close_dlg)
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            
            # 대화상자를 페이지에 표시
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
            return False
        return True
    
    def close_dlg(self, e):
        # 대화상자 닫기
        self.page.dialog.open = False
        self.page.update()
        
    def update_prefix(self):
        if self.mode == "link":
            #self.text_field.value = "http`s://www.sciencetimes.co.kr/",
            # 웹페이지 URL
            #url = "https://www.sciencetimes.co.kr/news/%eb%82%b4-%ec%a3%bc%eb%b3%80-%ec%83%9d%eb%ac%bc-%ec%86%8c%eb%a6%ac%eb%a1%9c-%ec%83%9d%eb%ac%bc%eb%8b%a4%ec%96%91%ec%84%b1-%ec%97%b0%ea%b5%ac%ed%95%9c%eb%8b%a4%ec%86%8c%eb%a6%ac/?cat=31"
            if self.validate_input():
                response = requests.get(self.text_field.value)
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                view_content = soup.find(class_='view_content')

                if view_content:
                    response = requests.get(self.text_field.value)
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    view_content = soup.find(class_='view_content')
                    paragraphs = []

                    if view_content:
                        # view_content 내의 모든 <p> 태그를 찾아 텍스트 추출
                        for p in view_content.find_all('p'):
                            paragraph_text = p.get_text(strip=True)
                            if paragraph_text:  # 빈 문단 제외
                                paragraphs.append(paragraph_text)
                                    # 결과 출력
                        print(f"총 {len(paragraphs)}개의 문단을 찾았습니다.")
                        for i, para in enumerate(paragraphs, 1):
                            print(f"문단 {i}: {para[:50]}...")  # 각 문단의 처음 50자만 출력

                    else:
                        # Flet 경고창으로 대체
                        dlg = ft.AlertDialog(
                            title=ft.Text("오류"),
                            content=ft.Text("view_content 클래스를 찾을 수 없습니다."),
                            actions=[
                                ft.TextButton("확인", on_click=self.close_dlg)
                            ],
                            actions_alignment=ft.MainAxisAlignment.END,
                        )
                        self.page.dialog = dlg
                        dlg.open = True
                        self.page.update()
                else:
                    # Flet 경고창으로 대체
                    dlg = ft.AlertDialog(
                        title=ft.Text("오류"),
                        content=ft.Text("view_content 클래스를 찾을 수 없습니다."),
                        actions=[
                            ft.TextButton("확인", on_click=self.close_dlg)
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
                    self.page.dialog = dlg
                    dlg.open = True
                    self.page.update()

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

