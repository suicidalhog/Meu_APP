# views/template_list.py
import flet as ft
from core.database import Database
from views.edit_template import EditTemplate
from core.template_exporter import export_template_pdf
import os, platform, subprocess

class TemplateList(ft.Column):
    def __init__(self, page):
        super().__init__(spacing=10, scroll=ft.ScrollMode.AUTO)
        self.page = page
        self.db = Database()

        self.controls.append(ft.Text("Templates Clínicos", size=26, weight=ft.FontWeight.BOLD))
        self.template_container = ft.Column()
        self.controls.append(self.template_container)

        self.controls.append(ft.ElevatedButton("Criar Novo Template", icon=ft.icons.ADD, on_click=self.novo_template))

        self.page.on_keyboard_event = self.handle_keyboard

        self.load_templates()

    def handle_keyboard(self, e):
        if e.ctrl and e.key == "n":
            self.novo_template(e)

    def load_templates(self):
        transtornos = self.db.listar_templates()
        self.template_container.controls.clear()

        if not transtornos:
            self.template_container.controls.append(ft.Text("Nenhum template disponível."))
        else:
            for nome in transtornos:
                self.template_container.controls.append(
                    ft.Row([
                        ft.Text(nome, size=16, expand=True),
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, n=nome: self.editar(n)),
                        ft.IconButton(icon=ft.icons.PICTURE_AS_PDF, tooltip="Exportar PDF", on_click=lambda e, n=nome: self.exportar(n))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )

        self.page.update()

    def editar(self, nome):
        self.page.controls.clear()
        self.page.add(EditTemplate(self.page, nome))
        self.page.update()

    def exportar(self, nome):
        caminho = export_template_pdf(nome)
        if caminho:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Exportado: {caminho}"))
            self.page.snack_bar.open = True
            self.page.update()
            try:
                if platform.system() == "Windows":
                    os.startfile(caminho)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", caminho])
                else:
                    subprocess.run(["xdg-open", caminho])
            except Exception as ex:
                print(f"Erro ao abrir PDF: {ex}")

    def novo_template(self, e):
        def criar(te):
            nome = campo_nome.value.strip()
            existentes = self.db.listar_templates()
            if nome in existentes:
                self.page.snack_bar = ft.SnackBar(ft.Text("Nome de template já existe."))
                self.page.snack_bar.open = True
                self.page.update()
                return
            if nome:
                dialog.open = False
                self.page.controls.clear()
                self.page.add(EditTemplate(self.page, transtorno=nome))
                self.page.update()

        campo_nome = ft.TextField(label="Nome do novo template")
        dialog = ft.AlertDialog(
            title=ft.Text("Novo Template"),
            content=campo_nome,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Criar", on_click=criar)
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
