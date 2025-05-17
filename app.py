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