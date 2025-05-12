# views/edit_template.py (com botão de exportação para PDF)
import flet as ft
from core.database import Database
from core.template_exporter import export_template_pdf

class EditTemplate(ft.Column):
    def __init__(self, page, transtorno=""):
        super().__init__(spacing=10, scroll=ft.ScrollMode.AUTO)
        self.page = page
        self.transtorno = transtorno
        self.db = Database()

        self.campos = []
        self.campos_container = ft.Column()

        self.controls.append(ft.Text(f"Editar Template: {transtorno}", size=24, weight=ft.FontWeight.BOLD))
        self.controls.append(self.campos_container)
        self.controls.append(ft.ElevatedButton("Adicionar Campo", icon=ft.icons.ADD, on_click=self.adicionar_campo))
        self.controls.append(ft.ElevatedButton("Salvar Template", icon=ft.icons.SAVE, on_click=self.salvar_template))
        self.controls.append(ft.ElevatedButton("Exportar como TXT", icon=ft.icons.DOWNLOAD, on_click=self.exportar_txt))
        self.controls.append(ft.ElevatedButton("Exportar como PDF", icon=ft.icons.PICTURE_AS_PDF, on_click=self.exportar_pdf))
        self.controls.append(ft.ElevatedButton("Duplicar Template", icon=ft.icons.COPY, on_click=self.duplicar_template))
        self.controls.append(ft.ElevatedButton("Voltar", icon=ft.icons.ARROW_BACK, on_click=self.voltar))

        self.load_template()
        self.page.on_keyboard_event = self.handle_keyboard

    def load_template(self):
        texto = self.db.buscar_template_por_transtorno(self.transtorno)
        if not texto:
            return

        for linha in texto.split("\n"):
            if not linha.strip():
                continue
            tipo, rotulo, variavel, *resto = linha.split(",")
            linhas = int(resto[0]) if resto else 1
            self.adicionar_campo_manual(tipo.strip(), rotulo.strip(), variavel.strip(), linhas)

    def adicionar_campo_manual(self, tipo, rotulo, variavel, linhas):
        tipo_dropdown = ft.Dropdown(label="Tipo", options=[ft.dropdown.Option("texto"), ft.dropdown.Option("checkbox"), ft.dropdown.Option("escala")], value=tipo)
        campo_rotulo = ft.TextField(label="Rótulo", value=rotulo)
        campo_variavel = ft.TextField(label="Variável", value=variavel)
        campo_linhas = ft.TextField(label="Linhas", value=str(linhas), visible=(tipo=="texto"))

        def tipo_changed(e):
            campo_linhas.visible = tipo_dropdown.value == "texto"
            self.page.update()

        tipo_dropdown.on_change = tipo_changed

        linha = ft.Row([
            tipo_dropdown,
            campo_rotulo,
            campo_variavel,
            campo_linhas,
            ft.IconButton(icon=ft.icons.DELETE, tooltip="Remover", on_click=lambda _: self.remover_campo(linha))
        ], alignment=ft.MainAxisAlignment.START)

        self.campos.append((linha, tipo_dropdown, campo_rotulo, campo_variavel, campo_linhas))
        self.campos_container.controls.append(linha)
        self.page.update()

    def adicionar_campo(self, e):
        self.adicionar_campo_manual("texto", "", "", 1)

    def remover_campo(self, linha):
        self.campos = [(l, t, r, v, n) for (l, t, r, v, n) in self.campos if l != linha]
        self.campos_container.controls.remove(linha)
        self.page.update()

    def salvar_template(self, e):
        linhas = []
        for _, tipo, rotulo, variavel, campo_linhas in self.campos:
            t = tipo.value or ""
            r = rotulo.value or ""
            v = variavel.value or ""
            l = campo_linhas.value or "1"
            linhas.append(f"{t},{r},{v},{l}")

        template_txt = "\n".join(linhas)
        self.db.salvar_template(self.transtorno, template_txt)

        self.page.snack_bar = ft.SnackBar(ft.Text("Template salvo com sucesso!"))
        self.page.snack_bar.open = True
        self.page.update()

    def exportar_txt(self, e):
        linhas = []
        for _, tipo, rotulo, variavel, campo_linhas in self.campos:
            t = tipo.value or ""
            r = rotulo.value or ""
            v = variavel.value or ""
            l = campo_linhas.value or "1"
            linhas.append(f"{t},{r},{v},{l}")

        texto = "\n".join(linhas)
        filename = f"template_{self.transtorno.replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(texto)

        self.page.snack_bar = ft.SnackBar(ft.Text(f"Exportado como {filename}"))
        self.page.snack_bar.open = True
        self.page.update()

    def voltar(self, e):
        self.page.go("/templates")

    def duplicar_template(self, e):
        def confirmar_duplicacao(te):
            novo_nome = campo_nome.value.strip()
            if not novo_nome:
                return
            existentes = self.db.listar_templates()
            if novo_nome in existentes:
                self.page.snack_bar = ft.SnackBar(ft.Text("Já existe um template com esse nome."))
                self.page.snack_bar.open = True
                self.page.update()
                return
            linhas = []
            for _, tipo, rotulo, variavel, campo_linhas in self.campos:
                t = tipo.value or ""
                r = rotulo.value or ""
                v = variavel.value or ""
                l = campo_linhas.value or "1"
                linhas.append(f"{t},{r},{v},{l}")
            self.db.salvar_template(novo_nome, "".join(linhas))
            dialog.open = False
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Template duplicado como '{novo_nome}'"))
            self.page.snack_bar.open = True
            self.page.update()

        campo_nome = ft.TextField(label="Novo nome para o template")
        dialog = ft.AlertDialog(
            title=ft.Text("Duplicar Template"),
            content=campo_nome,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Confirmar", on_click=confirmar_duplicacao)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def handle_keyboard(self, e):
        if e.ctrl and e.key == "s":
            self.salvar_template(e)
        elif e.ctrl and e.key == "e":
            self.exportar_pdf(e)
        elif e.ctrl and e.shift and e.key == "n":
            self.adicionar_campo(None)
        elif e.ctrl and e.key == "d":
            self.duplicar_template(None)
        elif e.ctrl and e.key == "t":
            self.exportar_txt(None)
        elif e.ctrl and e.key == "v":
            self.voltar(None)
        elif e.ctrl and e.key == "x":
            self.remover_campo(None)
        self.page.update()
        e.prevent_default()
        e.stop_propagation()
        e.handled = True
        self.page.update()