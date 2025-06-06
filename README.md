# 🧙‍♂️ Chat IA - Mundo Mágico de Harry Potter

Bem-vindo ao repositório do **Chat IA Temático de Harry Potter**!  
Este projeto foi desenvolvido como uma aplicação web interativa onde os usuários podem conversar com uma inteligência artificial ambientada no universo mágico de Hogwarts.

## ✨ Sobre o Projeto

Nosso chat utiliza inteligência artificial para responder aos usuários perguntas do mundo de **Harry Potter**. O sistema entende perguntas relacionadas ao universo bruxo e responde de forma coerente com o tema, proporcionando uma experiência imersiva e divertida.

### 🧰 Tecnologias Utilizadas

* **Python & Flask**: Estrutura principal da aplicação web e gerenciamento de rotas/sessões.
* **Socket.IO**: Atualização em tempo real do chat.
* **Google Gemini (via LangChain)**: Geração de respostas temáticas e avaliação de qualidade das respostas.
* **FAISS + Embeddings**: Busca inteligente em documentos baseados no universo de Harry Potter.
* **HTML & CSS**: Interface web do chat.
* **Dotenv**: Gerenciamento de variáveis sensíveis como a chave da API.

## 🚀 Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/chat-harry-potter.git
   cd chat-harry-potter
   ````

2. Crie um ambiente virtual e ative:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure a chave de API da Gemini (Google AI) no arquivo `.env` ou diretamente no script.

5. Inicie o servidor Flask:

   ```bash
   flask run
   ```

6. Acesse no navegador:
   [http://localhost:5000](http://localhost:5000)

## 👥 Integrantes

* Ana Beatriz Romera
* Artur Cassuriaga
* Nicolas Albano
* Samira Campos
* Sophie Kumagai

## 🧠 Exemplo de Perguntas

* Quem é Harry Potter?
* Como é voar em uma vassoura?
* Você conhece o Dumbledore?
* Me diga um feitiço para abrir portas!

A IA responderá de forma criativa e contextual, de acordo com arquivo contendo informações base (harryPotter.txt). ✨
