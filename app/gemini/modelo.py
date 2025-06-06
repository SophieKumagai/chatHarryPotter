import google.generativeai as genai
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

# Carrega a variável de ambiente do arquivo .env (se você estiver usando .env)
load_dotenv()

# Configura a API key
chave_api = os.getenv("GEMINI_API_KEY")

genai.configure(api_key = chave_api)

# pegar documentos
pasta = "documentos"
# Carrega todos os documentos .txt da pasta
def carregar_documentos(pasta):
    docs = []
    for nome in os.listdir(pasta):
        if nome.endswith(".txt"):
            caminho = os.path.join(pasta, nome)
            loader = TextLoader(caminho, encoding="utf-8")
            docs.extend(loader.load())
    return docs

documentos = carregar_documentos(pasta)
print(f"{len(documentos)} documentos carregados.")

# Dividir documentos em pedaços menores
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs_divididos = splitter.split_documents(documentos)
print(f"{len(docs_divididos)} fragmentos gerados.")

# Carregar embeddings do Gemini
embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=chave_api,
    model="models/embedding-001"
    )

# Criar vetor FAISS
db = FAISS.from_documents(docs_divididos, embeddings)

# Inicia o modelo
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.5,
    google_api_key=chave_api
)

# Cria o chain de pergunta-resposta com recuperação
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    return_source_documents=True
)

# rotina para enviar pergunta ao modelo
def responder_pergunta(pergunta: str) -> str:
    resposta = rag_chain(pergunta)
    return resposta["result"]
