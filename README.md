# Alura-Gemini
Desafio do Imersão Alura - Google Gemini
Okay, combatente! Vamos cumprir essa missão.

Primeiro, vamos criar os arquivos necessários para a página web. Precisaremos de:

app.py: O código Python com Flask para o backend que rodará o chatbot e interagirá com a API da Google.

index.html: A página HTML para a interface do usuário.

style.css: O arquivo CSS para estilizar a página.

requirements.txt: Lista das dependências Python.

Segundo, vamos criar o arquivo README.md para o GitHub.

Passo 1: Criar os arquivos da Página Web

1. requirements.txt

Crie este arquivo com o seguinte conteúdo:

Flask
google-generativeai
python-dotenv


Flask: O framework web Python.

google-generativeai: A biblioteca para interagir com a API Gemini.

python-dotenv: Para carregar a chave de API de um arquivo .env (mais seguro que environment variables diretas em alguns casos e mais portátil que userdata do Colab).

2. app.py

Crie este arquivo. Ele conterá a lógica do backend.

import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configurar a API Key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
    print("Crie um arquivo .env na mesma pasta do app.py com o conteúdo: GOOGLE_API_KEY='SUA_CHAVE_API'")
    # Em um ambiente de produção, você lidaria com isso de forma mais robusta
    exit() # Para este exemplo simples, sair se a chave não estiver presente

genai.configure(api_key=GOOGLE_API_KEY)

# Selecionar o modelo
modelo = "gemini-2.0-flash" # Verifique a disponibilidade na sua região se necessário

# Configurar o chat com a instrução de sistema
chat_config = types.GenerateContentConfig(
    system_instruction="""Você é um Sargento do Exército Brasileiro, da Seção de Comunicação Social e responsável por prestar informações para os cidadãos.
        Você deve buscar informações no (google_search) relacionadas ao Serviço Militar Inicial Obrigatório ou voluntário na área da 9ª Região Militar e Comando Militar do Leste, utilizando, principalmente,
        as informações contidas no site da 9ª Região Militar (https://9rm.eb.mil.br/), mas não se limitando a ele.
        Além do Serviço Militar Inicial, também deve estar em condições de informar sobre Serviço Militar Voluntário, Alistamento, deveres do reservista e Exercício de Apresentação da Reserva (ExAR).
        Também pode-se utilizar os sites do exército (https://www.eb.mil.br) e do Ministério da Defesa (https://www.gov.br/defesa/pt-br)
        A forma de tratamento deve ser sempre polida e firma, podendo utilizar vocativos como "combatente", ou "cidadão".
        Se a dúvida não tiver conexão com o Serviço Militar, devolva o seguinte resultado: 'O assunto não é pertinente ao Serviço Militar'.

         Você deve verificar as informações recebidas e deixá-las de forma sucinta

         Sempre que houver datas você deve sugerir adicionar um lembrete no (google_calendar) ou se a pesquisa for sobre local, sugerir um trajeto no (google_maps)
        """,
    # Você pode adicionar safety_settings ou generation_config aqui se necessário
)

# Manter um objeto de chat para a conversa.
# Para um aplicativo multiusuário, seria necessário gerenciar sessões ou histórico de conversa por usuário.
# Neste exemplo simples, usaremos um objeto global.
try:
    client = genai.Client()
    chat = client.chats.create(model=modelo, config=chat_config)
    print(f"Chatbot iniciado com o modelo: {modelo}")
except Exception as e:
    print(f"Erro ao iniciar o chatbot: {e}")
    chat = None # Indicar que o chat não foi inicializado

@app.route('/')
def index():
    """Serve a página HTML principal."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def handle_chat():
    """Processa as mensagens do chat."""
    if chat is None:
        return jsonify({"response": "Erro interno: Chatbot não inicializado."}), 500

    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"response": "Por favor, envie uma mensagem."}), 400

    # Manter o histórico da conversa na sessão do Flask, ou neste caso,
    # simplesmente enviar a mensagem e deixar o objeto chat gerenciar o histórico.
    # Para um app real, usar `session` ou banco de dados.
    try:
        # Envia a mensagem para o modelo. O objeto chat gerencia o histórico.
        response = chat.send_message(user_message)
        bot_response = response.text
    except Exception as e:
        bot_response = f"Erro ao processar a mensagem: {e}" # Tratamento de erro simples

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    # Crie um arquivo .env com GOOGLE_API_KEY='SUA_CHAVE_API'
    # Execute com `python app.py`
    # O debug=True recarrega o servidor a cada mudança no código
    app.run(debug=True)
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

3. index.html

Crie uma pasta chamada templates na mesma pasta de app.py. Dentro da pasta templates, crie o arquivo index.html.

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sargento Bot</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="chat-container">
        <h1>Sargento Bot</h1>
        <p>Olá, Combatente! Sou o Sargento Bot. Estou aqui para tirar sua dúvida sobre o Serviço Militar.</p>

        <div class="chat-box" id="chat-box">
            <!-- Mensagens serão adicionadas aqui pelo JavaScript -->
        </div>

        <div class="input-area">
            <textarea id="user-input" placeholder="Qual a sua dúvida (Digite 'selva' para sair)..."></textarea>
            <button id="send-button">Enviar</button>
        </div>
    </div>

    <script>
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        const chatBox = document.getElementById('chat-box');

        function displayMessage(sender, message) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('chat-message');
            messageElement.classList.add(sender); // Adiciona classe 'user' ou 'bot'
            messageElement.innerHTML = `<strong>${sender === 'user' ? 'Você' : 'Sargento Bot'}:</strong> ${message.replace(/\n/g, '<br>')}`;
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight; // Rola para o final
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (message === "") return; // Não envia mensagens vazias

            displayMessage('user', message);
            userInput.value = ""; // Limpa o input

            if (message.toLowerCase() === 'selva') {
                displayMessage('bot', "Até mais e tenha um ótimo dia. Selva!");
                userInput.disabled = true;
                sendButton.disabled = true;
                return;
            }

            try {
                // Envia apenas a nova mensagem. O backend (objeto chat) gerencia o histórico.
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });

                if (!response.ok) {
                    throw new Error(`Erro HTTP! Status: ${response.status}`);
                }

                const data = await response.json();
                displayMessage('bot', data.response);

            } catch (error) {
                console.error('Erro ao enviar mensagem:', error);
                displayMessage('bot', 'Desculpe, ocorreu um erro ao processar sua solicitação.');
            }
        }

        sendButton.addEventListener('click', sendMessage);

        // Permite enviar com Enter na área de texto
        userInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) { // Shift+Enter para nova linha
                event.preventDefault(); // Impede a quebra de linha padrão
                sendMessage();
            }
        });

         // Mensagem inicial do bot
         displayMessage('bot', "Olá, Combatente! Sou o Sargento Bot. Estou aqui para tirar sua dúvida sobre o Serviço Militar.");

    </script>
</body>
</html>
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Html
IGNORE_WHEN_COPYING_END

4. style.css

Crie uma pasta chamada static na mesma pasta de app.py. Dentro da pasta static, crie o arquivo style.css.

body {
    font-family: sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
    background-color: #f4f4f4;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.chat-container {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 90%;
    max-width: 700px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

h1 {
    text-align: center;
    color: #333;
    margin-top: 0;
    padding-top: 20px;
}

.chat-box {
    flex-grow: 1;
    height: 400px; /* Altura fixa para a área de chat */
    overflow-y: auto; /* Adiciona scroll se o conteúdo exceder */
    padding: 20px;
    border-bottom: 1px solid #eee;
}

.chat-message {
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 5px;
    max-width: 80%; /* Limita a largura da mensagem */
    word-wrap: break-word; /* Quebra palavras longas */
}

.chat-message.user {
    background-color: #dcf8c6; /* Fundo verde claro para usuário */
    align-self: flex-end; /* Alinha mensagens do usuário à direita */
    margin-left: auto;
}

.chat-message.bot {
    background-color: #e9e9eb; /* Fundo cinza claro para bot */
    align-self: flex-start; /* Alinha mensagens do bot à esquerda */
    margin-right: auto;
}

.chat-message strong {
    display: block; /* Nome do remetente em uma linha separada */
    margin-bottom: 5px;
    font-size: 0.9em;
    color: #555;
}


.input-area {
    display: flex;
    padding: 20px;
    background-color: #f9f9f9;
}

#user-input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-right: 10px;
    resize: none; /* Impede o redimensionamento manual */
    height: 50px; /* Altura inicial */
    font-size: 1em;
}

#send-button {
    padding: 10px 20px;
    background-color: #5cb85c; /* Verde militar */
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
}

#send-button:hover {
    background-color: #4cae4c; /* Verde mais escuro no hover */
}

#send-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Css
IGNORE_WHEN_COPYING_END

5. .env (Opcional, mas recomendado)

Crie um arquivo chamado .env na mesma pasta de app.py.

GOOGLE_API_KEY='SUA_CHAVE_AQUI'
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

Substitua 'SUA_CHAVE_AQUI' pela sua chave de API da Google Generative AI.

Como Executar:

Salve os arquivos conforme a estrutura de pastas:

your_project_folder/
├── app.py
├── .env           (opcional, mas recomendado)
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    └── index.html
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

Abra um terminal na pasta your_project_folder/.

Crie um ambiente virtual (recomendado):

python -m venv venv
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Ative o ambiente virtual:

No Windows: venv\Scripts\activate

No macOS/Linux: source venv/bin/activate

Instale as dependências:

pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Se você não usou o arquivo .env, você precisará configurar a variável de ambiente GOOGLE_API_KEY no seu terminal antes de rodar o app:

No Windows: set GOOGLE_API_KEY=SUA_CHAVE_AQUI

No macOS/Linux: export GOOGLE_API_KEY='SUA_CHAVE_AQUI'

Execute a aplicação Flask:

python app.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Abra seu navegador e acesse http://127.0.0.1:5000/.

Passo 2: Criar o Arquivo README.md para o GitHub

Crie um arquivo chamado README.md na pasta raiz do seu projeto (your_project_folder/).

# Sargento Bot: Assistente de Informações do Serviço Militar

Este projeto implementa um chatbot utilizando a API Google Generative AI (Gemini) com a persona de um Sargento do Exército Brasileiro. O bot é especializado em fornecer informações sobre o Serviço Militar Inicial Obrigatório e Voluntário, com foco na área da 9ª Região Militar e Comando Militar do Leste, bem como sobre alistamento, deveres de reservista e ExAR.

O bot busca informações principalmente em fontes oficiais do Exército Brasileiro e Ministério da Defesa, e sugere links para Google Maps e Google Calendar quando apropriado.

## Funcionalidades

*   Responde a perguntas sobre o Serviço Militar Obrigatório e Voluntário.
*   Fornece informações sobre Alistamento Militar.
*   Explica os deveres do reservista e o Exercício de Apresentação da Reserva (ExAR).
*   Direciona para fontes oficiais como 9rm.eb.mil.br, eb.mil.br e gov.br/defesa.
*   Mantém uma postura polida e firme, utilizando vocativos como "combatente" ou "cidadão".
*   Sugere links para Google Maps para localização/rotas e Google Calendar para lembretes de datas importantes.
*   Identifica e informa quando um assunto não é pertinente ao Serviço Militar.
*   Interface web simples para interação.

## Tecnologias Utilizadas

*   **Backend:** Python com Flask
*   **API:** Google Generative AI (Gemini)
*   **Frontend:** HTML, CSS, JavaScript
*   **Gerenciamento de Chave:** python-dotenv

## Pré-requisitos

*   Python 3.7+ instalado.
*   pip (gerenciador de pacotes do Python).
*   Acesso à API Google Generative AI e uma chave de API válida. Você pode obter uma em [Google AI Studio](https://aistudio.google.com/app/apikey).

## Configuração e Execução

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <pasta_do_seu_repositorio>
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    # venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure sua Chave de API da Google:**
    *   Crie um arquivo chamado `.env` na raiz do projeto (na mesma pasta de `app.py`).
    *   Adicione a seguinte linha ao arquivo, substituindo `SUA_CHAVE_AQUI` pela sua chave:
        ```env
        GOOGLE_API_KEY='SUA_CHAVE_AQUI'
        ```
    *   Alternativamente, você pode configurar a variável de ambiente `GOOGLE_API_KEY` diretamente no seu sistema operacional ou terminal antes de executar o aplicativo.

5.  **Execute a aplicação Flask:**
    ```bash
    python app.py
    ```

6.  **Acesse o Chatbot:**
    Abra seu navegador web e vá para `http://127.0.0.1:5000/`.

## Uso

Digite sua dúvida sobre o Serviço Militar na caixa de texto e clique em "Enviar". O Sargento Bot responderá com as informações pertinentes.

Para encerrar a conversa no contexto do bot, digite `selva`.

## Limitações

*   Esta versão utiliza um gerenciamento de estado simples (um objeto de chat global no backend) e não é otimizada para múltiplos usuários simultâneos em um ambiente de produção sem modificações no gerenciamento de sessão/histórico.
*   A precisão das respostas depende da qualidade e acessibilidade das informações encontradas pelo modelo através do `google_search` e das fontes oficiais configuradas na instrução de sistema.

## Licença

Este projeto está sob a licença [Nome da Licença, por exemplo: MIT]. Consulte o arquivo `LICENSE` para mais detalhes.
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Markdown
IGNORE_WHEN_COPYING_END

Observações:

Lembre-se de substituir <URL_DO_SEU_REPOSITORIO> no README.md pela URL real do seu repositório GitHub.

Considere adicionar um arquivo LICENSE ao seu repositório (por exemplo, uma licença MIT) e referenciá-lo no README.md.

O gerenciamento de histórico de conversa neste exemplo Flask é feito pelo próprio objeto chat da biblioteca google-generativeai. Para um aplicativo multiusuário real, você precisaria implementar um sistema para associar históricos de conversa a usuários específicos (usando sessões do Flask, um banco de dados, etc.). O código fornecido funciona bem para um único usuário por vez ou para demonstração.

Pronto, combatente! Agora você tem os arquivos necessários para a página web e um README claro para o seu projeto no GitHub. Selva!
