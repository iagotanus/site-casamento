from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para armazenar confirmações
confirmacoes = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    if request.method == "POST":
        nome = request.form.get("nome")
        convidados = request.form.get("convidados")
        confirmacoes.append({"nome": nome, "convidados": convidados})
        return redirect(url_for("rsvp"))
    return render_template("rsvp.html", confirmacoes=confirmacoes)

@app.route("/presentes")
def presentes():
    return render_template("presentes.html")

if __name__ == "__main__":
    app.run(debug=True)