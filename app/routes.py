import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

EXERCICIOS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'exercicios.json')
TREINOS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'treinos.json')

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/treinos_da_semana')
def treinos_da_semana():
    return render_template('treinos_da_semana.html')

@main.route('/exercicios', methods=['GET', 'POST'])
def exercicios():
    if request.method == 'POST':
        nome = request.form.get('nome')
        grupo = request.form.get('grupo')
        imagem_file = request.files.get('imagem')

        if imagem_file:
            filename = secure_filename(imagem_file.filename)
            caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            imagem_file.save(caminho)
            caminho_relativo = os.path.join('uploads', filename)
        else:
            caminho_relativo = ""

        novo_exercicio = {
            'nome': nome,
            'grupo': grupo,
            'imagem': caminho_relativo
        }

        if os.path.exists(EXERCICIOS_FILE):
            with open(EXERCICIOS_FILE, 'r') as f:
                dados = json.load(f)
        else:
            dados = []

        dados.append(novo_exercicio)

        with open(EXERCICIOS_FILE, 'w') as f:
            json.dump(dados, f, indent=2)

        return redirect(url_for('main.exercicios'))

    if os.path.exists(EXERCICIOS_FILE):
        with open(EXERCICIOS_FILE, 'r') as f:
            dados = json.load(f)
    else:
        dados = []

    return render_template('exercicios.html', exercicios=dados)

@main.route('/treinos', methods=['GET', 'POST'])
def treinos():
    if os.path.exists(EXERCICIOS_FILE):
        with open(EXERCICIOS_FILE, 'r') as f:
            exercicios = json.load(f)
    else:
        exercicios = []

    if request.method == 'POST':
        data = request.form.get('data')
        exercicio = request.form.get('exercicio')
        peso = request.form.get('peso')

        novo_treino = {
            'data': data,
            'exercicio': exercicio,
            'peso': peso
        }

        if os.path.exists(TREINOS_FILE):
            with open(TREINOS_FILE, 'r') as f:
                treinos = json.load(f)
        else:
            treinos = []

        treinos.append(novo_treino)

        with open(TREINOS_FILE, 'w') as f:
            json.dump(treinos, f, indent=2)

        return redirect(url_for('main.treinos'))

    if os.path.exists(TREINOS_FILE):
        with open(TREINOS_FILE, 'r') as f:
            treinos = json.load(f)
    else:
        treinos = []

    return render_template('treinos.html', treinos=treinos, exercicios=exercicios)

@main.route('/excluir_exercicio/<int:index>', methods=['POST'])
def excluir_exercicio(index):
    if os.path.exists(EXERCICIOS_FILE):
        with open(EXERCICIOS_FILE, 'r') as f:
            dados = json.load(f)
    else:
        dados = []

    if 0 <= index < len(dados):
        exercicio = dados[index]
        # Apagar imagem se houver
        if exercicio.get("imagem"):
            imagem_path = os.path.join("app", "static", exercicio["imagem"])
            if os.path.exists(imagem_path):
                os.remove(imagem_path)

        # Remove da lista
        dados.pop(index)

        # Salva novamente
        with open(EXERCICIOS_FILE, 'w') as f:
            json.dump(dados, f, indent=2)

    return redirect(url_for('main.exercicios'))
@main.route('/treino_a')
def treino_a():
    return render_template('treino_a.html')

@main.route('/treino_b')
def treino_b():
    return render_template('treino_b.html')

@main.route('/treino_c')
def treino_c():
    return render_template('treino_c.html')
