from flask import Blueprint, render_template, request, session
from datetime import datetime
from app import socketio
import os
from app.gemini.modelo import responder_pergunta
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

bp = Blueprint("chat", __name__)

def registrar_log(origem, mensagem, chat_id):
    os.makedirs("logs", exist_ok=True)
    caminho = f"logs/chat_{chat_id}.log"
    mensagem = mensagem.strip()
    if mensagem:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{origem}] {mensagem}\n")
        html = f"[{timestamp}] [{origem}] {mensagem}"
        socketio.emit("nova_mensagem", {"html": html})
    
def carregar_historico():
    chat_id = session.get("chat_id")
    caminho = f"logs/chat_{chat_id}.log"
    linhas_coloridas = []
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = list(f.readlines())
            for linha in linhas:
                if "[USUÁRIO]" in linha:
                    cor = "red"
                elif "[ATENDENTE]" in linha:
                    cor = "blue"
                elif "[GEMINI]" in linha:
                    cor = "purple"
                else:
                    cor = "black"
                linhas_coloridas.append(f'<font color="{cor}">{linha.strip()}</font>')
    return linhas_coloridas

def avaliar_resposta(pergunta, resposta_tutor, prompt_juiz, juiz):
    mensagens = [
        SystemMessage(content=prompt_juiz),
        HumanMessage(content=f"Pergunta do aluno: {pergunta}\n\nResposta do tutor: {resposta_tutor}")
    ]
    return str(juiz.invoke(mensagens).content)

@bp.route("/")
def home():
    return render_template("index.html", title="Página Inicial")

@bp.route("/usuario", methods=["GET", "POST"])
def usuario():
    if "chat_id" not in session:
        session["chat_id"] = datetime.now().strftime("%Y%m%d-%H%M%S")
        registrar_log("SISTEMA", f"=== Início da Sessão {session['chat_id']} ===", session["chat_id"])

    if request.method == "POST":
        if "enviar" in request.form:
            msg = request.form["mensagem"]
            registrar_log("USUÁRIO", msg, session["chat_id"])

            # Se for uma pergunta, consulta o Gemini
            if msg.strip().endswith("?"):
                resposta = responder_pergunta(msg)

                # juiz
                juiz = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    temperature=0.3,
                    google_api_key=os.getenv("GEMINI_API_KEY")
                )

                prompt_juiz = '''
                Você é um avaliador imparcial. Sua tarefa é revisar a resposta de um tutor de IA para uma pergunta de um trouxa de Harry Potter.

                Critérios:
                - A resposta está correta de acordo com os livros de Harry Potter?
                - A resposta está clara?
                - A resposta tem sentido?

                Se a resposta for boa, diga “✅ Aprovado” e explique por quê.
                Se tiver problemas, diga “⚠️ Reprovado” e proponha uma versão melhorada.
                '''

                avaliacao = avaliar_resposta(msg, resposta, prompt_juiz, juiz)

                if "Aprovado" in avaliacao:
                    # após verificar se ocorreu alucinação, gravar a resposta no log da sessão
                    registrar_log("GEMINI", resposta, session["chat_id"])
                else:
                    registrar_log("GEMINI", resposta, session["chat_id"])
                    registrar_log("GEMINI - JUIZ", avaliacao, session["chat_id"])
        elif "encerrar" in request.form:
            registrar_log("SISTEMA", f"=== Fim da Sessão {session['chat_id']} ===", session["chat_id"])
            session.pop("chat_id", None)
    historico = carregar_historico()
    return render_template("usuario.html", historico=historico, title="Chat - Usuário")

@bp.route("/atendente", methods=["GET", "POST"])
def atendente():
    if "chat_id" not in session:
        session["chat_id"] = datetime.now().strftime("%Y%m%d-%H%M%S")
        registrar_log("SISTEMA", f"=== Início da Sessão {session['chat_id']} ===", session["chat_id"])

    if request.method == "POST":
        if "enviar" in request.form:
            msg = request.form["mensagem"]
            registrar_log("ATENDENTE", msg, session["chat_id"])
        elif "encerrar" in request.form:
            registrar_log("SISTEMA", f"=== Fim da Sessão {session['chat_id']} ===", session["chat_id"])
            session.pop("chat_id", None)
    historico = carregar_historico()
    return render_template("atendente.html", historico=historico, title="Chat - Atendente")
