# main.py (roteador principal com integração das telas)
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import flet as ft
from views.template_list import TemplateList
from views.edit_template import EditTemplate
from views.patient_form import PatientForm
from views.patient_history import PatientHistory
from views.SearchPatient import SearchPatient  # Certifique-se de que o nome do arquivo e classe estão corretos

# Função principal
def main(page: ft.Page):
    page.title = "App Clínico GPT"
    page.theme_mode = "light"  # Substitua por uma string
    page.window_maximized = True

    def route_change(route):
        page.views.clear()
        match page.route:
            case "/":
                page.views.append(
                    ft.View("/", controls=[
                        ft.Text("Bem-vindo ao sistema clínico", size=30),
                        ft.ElevatedButton("Primeira Consulta", on_click=lambda _: page.go("/primeira")),
                        ft.ElevatedButton("Consulta de Seguimento", on_click=lambda _: page.go("/seguimento")),
                        ft.ElevatedButton("Buscar Paciente", on_click=lambda _: page.go("/buscar")),
                        ft.ElevatedButton("Templates", on_click=lambda _: page.go("/templates")),
                    ])
                )
            case "/primeira":
                page.views.append(ft.View(route="/primeira", controls=[PatientForm(page, tipo="primeira")]))
            case "/seguimento":
                page.views.append(ft.View(route="/seguimento", controls=[PatientForm(page, tipo="seguimento")]))
            case "/buscar":
                page.views.append(ft.View(route="/buscar", controls=[SearchPatient(page)]))
            case "/templates":
                page.views.append(ft.View(route="/templates", controls=[TemplateList(page)]))
            case _ if page.route.startswith("/historico/"):
                nome = page.route.split("/historico/")[1]
                page.views.append(ft.View(route=page.route, controls=[PatientHistory(page, nome)]))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
