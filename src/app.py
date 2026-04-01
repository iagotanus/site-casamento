from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import pandas as pd
from io import BytesIO
import os
import requests
import json

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback")

# SENHA DE ACESSO À PÁGINA DE CONFIRMADOS
SENHA_ADMIN = "casamento2026"

# Lista de convidados (exemplo)
with open("static/convidados.json", "r", encoding="utf-8") as f:
    convidados_registrados = json.load(f)["convidados"]
confirmacoes = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    if request.method == "POST":
        nome = request.form.get("nome")
        presenca = request.form.get("presenca")

        convidado = next(
            (c for c in convidados_registrados if c["nome"] == nome),
            None
        )

        if convidado:
            # 🔍 verifica se já existe resposta
            existente = next(
                (c for c in confirmacoes if c["nome"] == nome),
                None
            )

            url = "https://script.google.com/macros/s/AKfycbx4DihLE3bLfDcKOXsnLD719PVCKMX_Q3uvGA_2PzpJvHZ13_F71IMUmwro-6domdbM/exec"

            dados = {
                "nome": nome,
                "presenca": presenca
            }

            try:
                requests.post(url, json=dados)
            except:
                print("Erro ao enviar para Google Sheets")

            if existente:
                # 🔄 ATUALIZA resposta
                existente["presenca"] = presenca

                if presenca == "sim":
                    flash("Sua presença foi atualizada para CONFIRMADA 🎉", "success")
                else:
                    flash("Sua resposta foi atualizada. Sentiremos sua falta! 💔", "info")

            else:
                # 🆕 NOVA resposta
                confirmacoes.append({
                    "nome": nome,
                    "presenca": presenca
                })

                if presenca == "sim":
                    flash("Presença confirmada com sucesso! 🎉", "success")
                else:
                    flash("Sentiremos sua falta! 💔", "info")

        else:
            flash("Nome e não confere.", "error")

        return redirect(url_for("rsvp"))

    return render_template("rsvp.html", convidados=convidados_registrados)

# LOGIN PARA CONFIRMADOS
@app.route("/login-confirmados", methods=["GET", "POST"])
def login_confirmados():
    if request.method == "POST":
        senha = request.form.get("senha")

        if senha == SENHA_ADMIN:
            session["admin_logado"] = True
            return redirect(url_for("confirmados"))
        else:
            flash("Senha incorreta.", "error")

    return render_template("login_confirmados.html")

# PÁGINA PROTEGIDA
@app.route("/confirmados")
def confirmados():
    if not session.get("admin_logado"):
        return redirect(url_for("login_confirmados"))

    return render_template("confirmados.html", confirmacoes=confirmacoes)

@app.route("/confirmados/excel")
def baixar_confirmados_excel():
    if not session.get("admin_logado"):
        return redirect(url_for("login_confirmados"))

    df = pd.DataFrame(confirmacoes)

    output = BytesIO()
    df.to_excel(output, index=False, sheet_name="Confirmados")
    output.seek(0)

    return send_file(
        output,
        download_name="confirmados_casamento.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route("/logout")
def logout():
    session.pop("admin_logado", None)
    return redirect(url_for("index"))

@app.route("/presentes")
def presentes():
    return render_template("presentes.html")

@app.route("/padrinhos")
def padrinhos():
    return render_template("padrinhos.html")

@app.route("/presente/<int:valor>")
def presente_pagamento(valor):
    qrs_disponiveis = {
        100: "pix_100.jpeg",
        125: "pix_125.jpeg",
        150: "pix_150.jpeg",
        200: "pix_200.jpeg",
        300: "pix_300.jpeg",
        350: "pix_350.jpeg",
        400: "pix_400.jpeg",
        500: "pix_500.jpeg",
        600: "pix_600.jpeg",
        650: "pix_650.jpeg",
        700: "pix_700.jpeg",
        1000: "pix_1000.jpeg",
    }

    qr = qrs_disponiveis.get(valor)

    if not qr:
        return "Valor inválido", 404

    return render_template(
        "presente_pagamento.html",
        valor=valor,
        qr=qr
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))