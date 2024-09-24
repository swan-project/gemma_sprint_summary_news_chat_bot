import flet as ft
from typing import Callable
from components.item import Item
import json

class ListView(ft.UserControl):
    def __init__(self, on_item_click: Callable[[Item], None]):
        super().__init__()
        self.on_item_click = on_item_click
        self.list_view = ft.ListView(
            width=800,
            height=600,  # 스크롤이 가능하도록 높이를 설정
            auto_scroll=True
        )
        self.empty_message = ft.Text(
            value="Empty saved summary",
            size=20,
            color=ft.colors.GREY_500,
            text_align=ft.TextAlign.CENTER
        )
        self.load_items()

    def load_items(self):
        self.list_view.controls.clear()
        items = self.read_items_from_local_storage()
        if not items:
            self.list_view.controls.append(self.empty_message)
        for item in items:
            self.list_view.controls.append(
                ft.ListTile(
                    title=ft.Row(
                        controls=[
                            ft.Text(item.title),
                            ft.Text(item.mode),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, item=item: self.delete_item(item)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    on_click=lambda e, item=item: self.click_item(item)
                )
            )

    def read_items_from_local_storage(self) -> list[Item]:
        try:
            with open("local_storage.json", "r") as f:
                data = json.load(f)
                return [Item(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def delete_item(self, item: Item):
        try:
            with open("local_storage.json", "r") as f:
                data = json.load(f)
            
            data = [i for i in data if i["id"] != item.id]
            
            with open("local_storage.json", "w") as f:
                json.dump(data, f, indent=4)
            
            print(f"Deleted item: {item.to_dict()}")
            
            # Refresh the ListView after deletion
            self.load_items()
        except Exception as e:
            print(f"Error deleting item: {e}")
        
        self.load_items()
        self.update()
        

    def click_item(self, item: Item):
        self.on_item_click(item)

    def reset(self, e):
        try:
            # 빈 리스트로 초기화
            with open("local_storage.json", "w") as f:
                json.dump([], f, indent=4)
            
            print("Local storage has been reset.")
            
            # ListView 새로고침
            self.load_items()
        except Exception as e:
            print(f"Error resetting local storage: {e}")
        
        self.update()

    def build(self):
        return self.list_view