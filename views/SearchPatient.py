import flet as ft
from core.database import Database

class SearchPatient(ft.Column):
    def __init__(self, page):
        super().__init__(spacing=10)
        self.page = page
        self.db = Database()

        # Campo de busca
        self.query_field = ft.TextField(label="Nome do paciente", on_submit=self.search)

        # Contêiner para exibir os resultados
        self.results_container = ft.Column(scroll=ft.ScrollMode.AUTO)

        # Botão para voltar à página inicial
        self.voltar_button = ft.ElevatedButton("Voltar", on_click=self.voltar_home)

        # Adicionando os controles à página
        self.controls = [
            ft.Row([self.query_field, ft.ElevatedButton("Buscar", on_click=self.search)]),
            self.results_container,
            self.voltar_button
        ]

    def search(self, e):
        termo = self.query_field.value
        resultados = self.db.buscar_pacientes(termo)
        self.results_container.controls.clear()

        if not resultados:
            self.results_container.controls.append(ft.Text("Nenhum paciente encontrado."))
        else:
            for paciente in resultados:
                nome = paciente['nome']
                self.results_container.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.TextButton(
                                text=f"{nome}",
                                on_click=lambda e, nome=nome: self.page.go(f"/historico/{nome}"),
                                style=ft.ButtonStyle(color=ft.colors.BLUE, padding=10)
                            ),
                            ft.IconButton(
                                icon=ft.icons.NOTE_ADD,
                                tooltip="Nova Consulta",
                                icon_color=ft.colors.GREEN,
                                on_click=lambda e, nome=nome: self.nova_consulta(nome)
                            )
                        ]),
                        padding=8
                    )
                )
        self.page.update()

    def nova_consulta(self, nome):
        self.page.session.set("paciente_nome", nome)
        self.page.go("/consulta")

    def voltar_home(self, e):
        self.page.go("/")