# core/database.py
import sqlite3
import os

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("dados_clinicos.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                data TEXT,
                anotacoes TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS templates (
                transtorno TEXT PRIMARY KEY,
                conteudo TEXT
            )
        """)
        self.conn.commit()

    def salvar_consulta(self, nome, data, anotacoes):
        self.cursor.execute("INSERT INTO pacientes (nome) VALUES (?)", (nome,))
        self.cursor.execute("INSERT INTO consultas (nome, data, anotacoes) VALUES (?, ?, ?)", (nome, data, anotacoes))
        self.conn.commit()

    def buscar_historico(self, nome):
        self.cursor.execute("SELECT data, anotacoes FROM consultas WHERE nome = ? ORDER BY id DESC", (nome,))
        return self.cursor.fetchall()

    def salvar_template(self, transtorno, conteudo):
        self.cursor.execute("REPLACE INTO templates (transtorno, conteudo) VALUES (?, ?)", (transtorno, conteudo))
        self.conn.commit()

    def buscar_template_por_transtorno(self, transtorno):
        self.cursor.execute("SELECT conteudo FROM templates WHERE transtorno = ?", (transtorno,))
        res = self.cursor.fetchone()
        return res[0] if res else ""

    def listar_templates(self):
        self.cursor.execute("SELECT transtorno FROM templates")
        return [row[0] for row in self.cursor.fetchall()]
