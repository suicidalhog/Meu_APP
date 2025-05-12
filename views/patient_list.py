# views/patient_list.py (atualizado com sugestão de transtorno ao iniciar nova consulta e integração com templates por transtorno)
import flet as ft
from core.database import Database
import threading
import time

TRASTORNOS_SUGERIDOS = {
    "João": "TAG",
    "Maria": "TDAH",
    "Carlos": "TDM"
}

class PatientList(ft.Column):
    def __init__(self, page):
        super().__init__(spacing=10)
        self.page = page
        self.db = Database()
        self.query_field = ft.TextField(label="Nome do paciente", on_submit=self.search)
        self.results_container = ft.Column(scroll=ft.ScrollMode.AUTO)

        # Temporizador
        self.time_left = 60 * 60  # 60 minutos
        self.timer_text = ft.Text("Tempo restante: 60:00", size=18, color=ft.colors.GREEN_700)
        self.add_time_button = ft.ElevatedButton("+5 min", on_click=self.add_five_minutes)

        self.controls = [
            ft.Row([
                self.query_field,
                ft.ElevatedButton("Buscar", on_click=self.search),
                ft.ElevatedButton("Voltar", on_click=self.voltar_home)
            ]),
            ft.Row([self.timer_text, self.add_time_button]),
            self.results_container
        ]

        self.start_timer()

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
                                text=f"{nome} - Nasc: {paciente['nascimento']} - Sexo: {paciente['sexo']}",
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
        transtorno_sugerido = TRASTORNOS_SUGERIDOS.get(nome, "")
        self.page.session.set("paciente_nome", nome)
        self.page.session.set("paciente_transtorno", transtorno_sugerido)

        # Integração ativa: o transtorno salvo será usado em PatientForm
        # para carregar campos via template (tipos: texto, checkbox, escala)

        self.page.go("/consulta")

    def voltar_home(self, e):
        import views.home_view as home_view
        self.page.controls.clear()
        self.page.add(home_view.HomeView(self.page))
        self.page.update()

    def start_timer(self):
        def countdown():
            while self.time_left > 0:
                mins, secs = divmod(self.time_left, 60)
                time_str = f"{mins:02}:{secs:02}"
                self.timer_text.value = f"Tempo restante: {time_str}"

                if self.time_left <= 600:
                    self.timer_text.color = ft.colors.RED
                elif self.time_left <= 900:
                    self.timer_text.color = ft.colors.AMBER
                else:
                    self.timer_text.color = ft.colors.GREEN_700

                self.page.update()
                time.sleep(1)
                self.time_left -= 1

        threading.Thread(target=countdown, daemon=True).start()

    def add_five_minutes(self, e):
        self.time_left += 300
        self.page.snack_bar = ft.SnackBar(ft.Text("+5 minutos adicionados!"))
        self.page.snack_bar.open = True
        self.page.update()
