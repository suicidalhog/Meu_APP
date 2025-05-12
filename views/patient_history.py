# views/patient_history.py
import flet as ft
from core.database import Database
from core.pdf_exporter import export_patient_consultas_pdf

class PatientHistory(ft.Column):
    def __init__(self, page, nome):
        super().__init__(spacing=10, scroll=ft.ScrollMode.AUTO)
        self.page = page
        self.nome = nome
        self.db = Database()

        self.controls.append(ft.Text(f"Histórico de Consultas: {self.nome}", size=22, weight=ft.FontWeight.BOLD))

        self.resultado = ft.Column(spacing=10)
        self.controls.append(self.resultado)

        self.exportar_btn = ft.ElevatedButton("Exportar Histórico em PDF", icon=ft.icons.PICTURE_AS_PDF, on_click=self.exportar_pdf)
        self.controls.append(self.exportar_btn)

        self.pdf_path = ft.TextField(label="Arquivo PDF gerado", visible=False, read_only=True)
        self.copy_btn = ft.IconButton(icon=ft.icons.CONTENT_COPY, visible=False, on_click=self.copiar)
        self.controls.append(ft.Row([self.pdf_path, self.copy_btn]))

        self.page.on_keyboard_event = self.handle_keyboard

        self.carregar_historico()

    def handle_keyboard(self, e):
        if e.ctrl and e.key == "p":
            self.exportar_pdf(e)

    def carregar_historico(self):
        consultas = self.db.buscar_historico(self.nome)
        if not consultas:
            self.resultado.controls.append(ft.Text("Nenhuma consulta encontrada."))
            self.page.update()
            return

        for data, texto in consultas:
            self.resultado.controls.append(ft.Text(f"🗓 {data}", weight=ft.FontWeight.BOLD))
            for linha in texto.split("\n"):
                self.resultado.controls.append(ft.Text(linha))
            self.resultado.controls.append(ft.Divider())

        self.page.update()

    def exportar_pdf(self, e):
        caminho = export_patient_consultas_pdf(self.nome)
        if caminho:
            self.pdf_path.value = caminho
            self.pdf_path.visible = True
            self.copy_btn.visible = True
            self.page.snack_bar = ft.SnackBar(ft.Text("Histórico exportado com sucesso!"))
            self.page.snack_bar.open = True
            self.page.update()

    def copiar(self, e):
        self.page.set_clipboard(self.pdf_path.value)
        self.page.snack_bar = ft.SnackBar(ft.Text("Caminho copiado."))
        self.page.snack_bar.open = True
        self.page.update()
