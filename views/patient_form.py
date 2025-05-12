# views/patient_form.py (com atalhos de teclado: Ctrl+S, Ctrl+P)
import flet as ft
from core.database import Database
from core.pdf_exporter import export_patient_consultas_pdf
from datetime import datetime

class PatientForm(ft.Column):
    def __init__(self, page, tipo="primeira", nome="", transtorno=""):
        super().__init__()
        self.page = page
        self.tipo = tipo
        self.nome = nome
        self.transtorno = transtorno or self.page.session.get("paciente_transtorno")
        if self.transtorno is None:
            self.transtorno = ""
        self.db = Database()

        self.campos_dinamicos = []
        self.controls.append(ft.Text(f"Consulta de {self.nome} ({self.transtorno})", size=20, weight=ft.FontWeight.BOLD))

        self.load_template_fields()

        self.controls.append(ft.ElevatedButton("Salvar no banco de dados", on_click=self.salvar_consulta))
        self.controls.append(ft.ElevatedButton("Exportar histórico em PDF", icon=ft.icons.PICTURE_AS_PDF, on_click=self.exportar_pdf))

        self.pdf_path_field = ft.TextField(label="Arquivo PDF gerado", visible=False, read_only=True, value="")
        self.copy_button = ft.IconButton(icon=ft.icons.CONTENT_COPY, tooltip="Copiar caminho", visible=False, on_click=self.copiar_caminho)
        self.controls.append(ft.Row([self.pdf_path_field, self.copy_button]))

        self.page.on_keyboard_event = self.handle_keyboard

    def handle_keyboard(self, e):
        if e.ctrl and e.key == "s":
            self.salvar_consulta(e)
        elif e.ctrl and e.key == "p":
            self.exportar_pdf(e)

    def load_template_fields(self):
        template = self.db.buscar_template_por_transtorno(self.transtorno)

        if not template:
            self.controls.append(ft.Text(f"Nenhum template encontrado para {self.transtorno}.", color=ft.Colors.RED))
            self.page.update()
            return

        for linha in template.split("\n"):
            if not linha.strip():
                continue
            tipo, rotulo, variavel, *resto = linha.split(",")
            tipo = tipo.strip().lower()
            rotulo = rotulo.strip()
            variavel = variavel.strip()
            linhas = int(resto[0].strip()) if resto else 1

            if tipo == "texto":
                campo = ft.TextField(label=rotulo, multiline=True, min_lines=linhas, key=variavel)
            elif tipo == "checkbox":
                campo = ft.Checkbox(label=rotulo, key=variavel)
            elif tipo == "escala":
                campo = ft.Slider(min=0, max=10, label=rotulo, divisions=10, key=variavel)
            else:
                campo = ft.Text(f"Tipo desconhecido: {tipo}", color=ft.Colors.ORANGE)

            self.campos_dinamicos.append((variavel, campo))
            self.controls.append(campo)

        self.page.update()

    def salvar_consulta(self, e):
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        anotacoes = []

        for variavel, widget in self.campos_dinamicos:
            valor = None
            if isinstance(widget, ft.TextField):
                valor = widget.value
            elif isinstance(widget, ft.Checkbox):
                valor = "Sim" if widget.value else "Não"
            elif isinstance(widget, ft.Slider):
                valor = str(int(widget.value or 0))

            if valor is not None:
                anotacoes.append(f"{variavel}: {valor}")

        nota_final = "\n".join(anotacoes)
        self.db.salvar_consulta(self.nome, data_atual, nota_final)

        self.page.snack_bar = ft.SnackBar(ft.Text("Consulta salva com sucesso!"))
        self.page.snack_bar.open = True
        self.page.update()
        self.page.go(f"/historico/{self.nome}")

    def exportar_pdf(self, e):
        path = export_patient_consultas_pdf(self.nome)
        if path:
            self.pdf_path_field.value = path
            self.pdf_path_field.visible = True
            self.copy_button.visible = True
            self.page.snack_bar = ft.SnackBar(ft.Text("PDF exportado com sucesso!"))
            self.page.snack_bar.open = True
            self.page.update()

    def copiar_caminho(self, e):
        self.page.set_clipboard(self.pdf_path_field.value)
        self.page.snack_bar = ft.SnackBar(ft.Text("Caminho copiado para a área de transferência"))
        self.page.snack_bar.open = True
        self.pdf_path_field.value = ""
        self.pdf_path_field.visible = False
        self.copy_button.visible = False
        self.page.update()
