from flask import Flask, g, render_template,\
    request, redirect, url_for, flash, session, make_response, jsonify


import hashlib
import os
import mysql.connector
import requests, json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


from models.usuario import Usuario
from models.usuarioDAO import UsuarioDAO
from models.exercicio import exercicio
from models.exercicioDAO import ExercicioDAO
from models.avaliacao import Avaliacao
from models.avaliacaoDAO import AvaliacaoDAO

app = Flask(__name__)
app.secret_key = "senha123"

DB_HOST = "localhost"
DB_USER = "root"
DB_NAME = "academiadb"
DB_PASS = ""

app.auth = {
    # acao: { perfil:permissao }
    'painel': {0:1, 1:1},
    'logout': {0:1, 1:1},
    'cadastrar_exercicio': {0:1, 1:1},
    'listar_exercicio': {0:1, 1:1},
    'cadastrar_saida': {0:1, 1:1}
}

@app.before_request
def autorizacao():
    acao = request.path[1:]
    acao = acao.split('/')
    if len(acao)>=1:
        acao = acao[0]

    acoes = app.auth.keys()
    if acao in list(acoes):
        if session.get('logado') is None:
            return redirect(url_for('login'))
        else:
            tipo = session['logado']
            if app.auth[acao] == 0:
                return redirect(url_for('painel'))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == "POST":
        # valor = request.form['campoHTML']
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario(nome, sobrenome, email, senha)

        dao = UsuarioDAO(get_db())
        codigo = dao.inserir(usuario)

        if codigo > 0:
            msg = ("Cadastrado com sucesso!")
        else:
            msg = ("Erro ao cadastrar!")

    vartitulo = "Cadastro"
    return render_template("register.html", titulo=vartitulo, msg=msg)


@app.route('/cadastrar_treino', methods=['GET', 'POST'])
def cadastrar_exercicios():
    if request.method == "POST":
        carga = request.form['carga']
        series = request.form['series']
        repeticoes = request.form['repeticoes']

        exercicios = exercicio(carga, series, repeticoes)

        dao = ExercicioDAO(get_db())
        codigo = dao.inserir(exercicios)

        if codigo > 0:
            flash("Cadastrado com sucesso! Código %d" % codigo, "success")
        else:
            flash("Erro ao cadastrar!", "danger")

    vartitulo = "Cadastro de Exercicio"
    return render_template("exercicio-cadastrar.html", titulo=vartitulo)

@app.route('/avaliacao', methods=['GET', 'POST'])
def avaliacao():
    if request.method == "POST":
        peso = request.form['peso']
        altura = request.form['altura']
        braco = request.form['braco']
        ombro = request.form['ombro']
        peito = request.form['peito']
        cintura = request.form['cintura']
        quadril = request.form['quadril']
        abdominal = request.form['abdominal']
        coxaMedial = request.form['coxaMedial']
        panturrilha = request.form['panturrilha']

        avaliacao = Avaliacao(peso, altura, braco, ombro, peito, cintura, quadril,
                              abdominal, coxaMedial, panturrilha,session['logado']['codigo'] )

        dao = AvaliacaoDAO(get_db())
        codigo = dao.inserir(avaliacao)

        if codigo > 0:
            flash("Cadastrado com sucesso! Código %d" % codigo, "success")
        else:
            flash("Erro ao cadastrar!", "danger")

    vartitulo = "Avaliacao"
    return render_template("avaliacao.html", titulo=vartitulo)

@app.route('/listar_exercicio', methods=['GET',])
def listar_exercicio():
    dao = ExercicioDAO(get_db())
    exercicios_db = dao.listar()
    return render_template("exercicio-listar.html", exercicios=exercicios_db)

@app.route('/listaraval', methods=['GET', 'POST'])
def listaraval():
    dao = AvaliacaoDAO(get_db())
    avaliacao_db = dao.listar()
    return render_template("listaraval.html", avaliacao=avaliacao_db)

@app.route('/cadastrar_saida', methods=['GET', 'POST'])
def cadastrar_saida():
    daoUsuario = UsuarioDAO(get_db())
    daoPlanta = PlantaDAO(get_db())

    if request.method == "POST":

        dtsaida = request.form['dtsaida']
        usuario = request.form['usuario']
        planta = request.form['planta']
        saida = Saida(usuario, planta, dtsaida)

        daoSaida = SaidaDAO(get_db())
        codigo = daoSaida.inserir(saida)
        if codigo > 0:
            flash("Saída cadastrada com sucesso! Código %d" % codigo, "success")
        else:
            flash("Erro ao registrar saída!", "danger")


    usuarios_db = daoUsuario.listar()
    plantas_db = daoPlanta.listar()
    return render_template("saida-cadastrar.html",
                           usuarios=usuarios_db, plantas=plantas_db)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        # Verificar dados
        dao = UsuarioDAO(get_db())
        usuario = dao.autenticar(email, senha)

        if usuario is not None:
            session['logado'] = {
                'codigo': usuario[0],
                'nome': usuario[3],
                'email': usuario[1],
            }
            return redirect(url_for('painel'))
        else:
            flash("Erro ao efetuar login!")

    return render_template("login.html", titulo="Login")


@app.route('/logout')
def logout():
    session['logado'] = None
    session.clear()
    return redirect(url_for('index'))

@app.route('/forgot')
def forgot():
    return render_template("forgot-password.html", titulo ="Esqueci minha senha")

@app.route('/painel')
def painel():
    return render_template("index.html", titulo="index")

@app.route('/peito', methods=['GET', 'POST'])
def peito():
    dao = ExercicioDAO(get_db())
    exercicio_db = dao.listar_peito()
    exercicio = list(exercicio_db)
    print(exercicio)

    video_url = [0, "https://www.youtube.com/embed/R08gYyypGto?si=ugbVi8tG0J354KOq"]
    return render_template("peito.html", titulo="peito", exercicio=exercicio, video_url = video_url)

@app.route('/perna', methods=['GET', 'POST'])
def perna():
    dao = ExercicioDAO(get_db())
    exercicio_db = dao.listar_perna()
    return render_template("perna.html", titulo="perna", exercicio=exercicio_db)

@app.route('/braco', methods=['GET', 'POST'])
def braco():
    dao = ExercicioDAO(get_db())
    exercicio_db = dao.listar_braco()
    return render_template("braco.html", titulo="braco", exercicio=exercicio_db)

@app.route('/costas', methods=['GET', 'POST'])
def costas():
    dao = ExercicioDAO(get_db())
    exercicio_db = dao.listar_costas()
    return render_template("costas.html", titulo="costas", exercicio=exercicio_db)

@app.route('/abdomen', methods=['GET', 'POST'])
def abdomen():
    dao = ExercicioDAO(get_db())
    exercicio_db = dao.listar_abdomen()
    return render_template("abdomen.html", titulo="abdomen", exercicio=exercicio_db)

@app.route('/alongamento', methods=['GET', 'POST'])
def alongamento():
    dao = ExercicioDAO(get_db())
    exercicio_db = dao.listar_alongamento()
    return render_template("alongamento.html", titulo="alongamento", exercicio=exercicio_db)

@app.route('/mainaval')
def mainaval():
    return render_template("mainaval.html", titulo="mainaval")

@app.route('/atualizar_avaliacao/<int:id>', methods=['POST'])
def atualizar_avaliacao(id):
    if request.method == "POST":
        peso = request.form['peso']
        altura = request.form['altura']
        braco = request.form['braco']
        ombro = request.form['ombro']
        peito = request.form['peito']
        cintura = request.form['cintura']
        quadril = request.form['quadril']
        abdominal = request.form['abdominal']
        coxaMedial = request.form['coxaMedial']
        panturrilha = request.form['panturrilha']

        from models.avaliacao import Avaliacao
        from models.avaliacaoDAO import AvaliacaoDAO

        avaliacao = Avaliacao(
            peso, altura, braco, ombro, peito, cintura, quadril,
            abdominal, coxaMedial, panturrilha, session['logado']['codigo']
        )

        dao = AvaliacaoDAO(get_db())
        sucesso = dao.atualizar(avaliacao, id)

        if sucesso:
            flash("Avaliação atualizada com sucesso!", "success")
        else:
            flash("Erro ao atualizar a avaliação!", "danger")

    return redirect(url_for('listaraval'))


@app.route('/teste-log')
def pagina_de_teste_log():
    print("\n--- ACESSANDO A ROTA DE TESTE /teste-log ---")

    db = get_db()
    dao = AvaliacaoDAO(db)

    print("1. Buscando dados na DAO...")
    resultados = dao.buscar_todas_avaliacoes_com_log()

    # Este print é crucial! Ele vai nos mostrar os dados brutos no terminal.
    print("2. Dados recebidos da DAO:")
    print(resultados)

    print("3. Renderizando o template 'teste.html'...")
    return render_template('teste.html', avaliacoes=resultados)

@app.route('/deletar_avaliacao/<int:id>')
def deletar_avaliacao(id):
    dao = AvaliacaoDAO(get_db())
    sucesso = dao.deletar(id)

    if sucesso:
        flash("Avaliação deletada com sucesso!", "success")
    else:
        flash("Erro ao deletar avaliação!", "danger")

    return redirect(url_for('listaraval'))

@app.route('/treinos', methods=['GET', 'POST'])
def treinos():
    dao = ExercicioDAO(get_db())
    exercicio_db = dao.listar_exercicios()
    return render_template("treinos.html", titulo="treinos", exercicio=exercicio_db)


@app.route('/criartreino', methods=['GET', 'POST'])
def criartreino():
    return render_template("criar_treino.html", titulo="criartreino")





@app.route('/get_exercises')
def get_exercises():
    try:

        dao = ExercicioDAO(get_db())
        exercicios = dao.listar_exercicios()

        # Converter para formato JSON
        exercicios_json = []
        for ex in exercicios:
            exercicios_json.append({
                'id': ex[0],
                'nome': ex[1],
                'descricao': ex[2],
                'equipamento': ex[3],
                'muscleGroup': ex[4],
                'video': ex[5]
            })
        return jsonify(exercicios_json)

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify([])


if __name__=='__main__':
    app.run(host="0.0.0.0", port=80, debug=True)