# 🧠 Sistema Clínico com Flet + SQLite

Interface moderna e responsiva para gerenciamento de consultas, pacientes e templates clínicos.

---

## 🚀 Como iniciar

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

---

## 📦 Requisitos

- Python 3.9+
- `flet`
- `fpdf`

```bash
pip install flet fpdf
```

---

## 🗂️ Estrutura
```
Meu_APP/
├── core/
│   ├── database.py         # Persistência
│   ├── pdf_exporter.py     # Exportação de consultas
│   ├── template_exporter.py# Exportação de templates
├── views/
│   ├── patient_form.py     # Formulário dinâmico de consulta
│   ├── patient_history.py  # Histórico de pacientes
│   ├── template_list.py    # Lista templates
│   ├── edit_template.py    # Editor visual
├── main.py                 # Roteador
├── run.py                  # Execução principal
```

---

## 🧭 Funcionalidades
- Consultas dinâmicas baseadas em transtornos
- Histórico completo por paciente
- Templates visuais com campos configuráveis
- Exportação em PDF e TXT
- Atalhos de teclado (Ctrl+S, Ctrl+P, Ctrl+E...)

---

## 🖼️ Capturas
*Adicione imagens ou gravações aqui se desejar*

---

## 👨‍⚕️ Desenvolvido para uso clínico com foco em agilidade e personalização.
