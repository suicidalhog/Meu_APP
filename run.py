# run.py
# Script de entrada para rodar a aplicação com Flet
import flet as ft
from main import main

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
