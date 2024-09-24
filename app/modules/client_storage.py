import flet as ft
import json

class ClientStorage:
    def __init__(self, page: ft.Page):
        self.page = page

    async def save_data(self, key: str, value: dict):
        """데이터를 client_storage에 저장합니다."""
        try:
            await self.page.client_storage.set(key, json.dumps(value))
            print(f"Data saved under key: {key}")
        except Exception as e:
            print(f"Error saving data: {e}")

    async def load_data(self, key: str):
        """client_storage에서 데이터를 불러옵니다."""
        try:
            data = await self.page.client_storage.get(key)
            if data:
                return json.loads(data)
            return None
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error loading data: {e}")
            return None

    async def delete_data(self, key: str):
        """client_storage에서 데이터를 삭제합니다."""
        try:
            await self.page.client_storage.remove(key)
            print(f"Data removed under key: {key}")
        except Exception as e:
            print(f"Error deleting data: {e}")

    async def reset_storage(self):
        """client_storage를 초기화합니다."""
        try:
            await self.page.client_storage.clear()
            print("Client storage has been reset.")
        except Exception as e:
            print(f"Error resetting client storage: {e}")
