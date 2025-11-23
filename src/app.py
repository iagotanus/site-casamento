from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"

# Lista de convidados (exemplo)
convidados_registrados = [
    {"nome": "Rosalina Camacho Tanus Ferreira", "cpf": "08408314807"},
    {"nome": "Maria Souza", "cpf": "98765432100"},
    {"nome": "Ana Oliveira", "cpf": "11122233344"},
]
confirmacoes = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")

        # Busca convidado
        encontrado = next((c for c in convidados_registrados if c["nome"] == nome and c["cpf"] == cpf), None)

        if encontrado:
            confirmacoes.append({"nome": nome})
            flash("Presença confirmada com sucesso! 🎉", "success")
        else:
            flash("Nome e CPF não conferem. Tente novamente.", "error")

        return redirect(url_for("rsvp"))

    return render_template("rsvp.html", convidados=convidados_registrados, confirmacoes=confirmacoes)

@app.route("/presentes")
def presentes():
    return render_template("presentes.html")

@app.route("/padrinhos")
def padrinhos():
    return render_template("padrinhos.html")



if __name__ == "__main__":
    app.run(debug=True)