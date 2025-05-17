import os
from flask import Flask, request, jsonify, render_template
from google import generativeai
# from google.generativeai import types # Não precisamos importar types aqui para esta configuração
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

# Configura a biblioteca com a chave de API
generativeai.configure(api_key=GOOGLE_API_KEY)

# Selecionar o modelo
# Verifique a disponibilidade na sua região se necessário. gemini-1.5-flash-latest é uma boa opção.
modelo = "gemini-1.5-flash-latest"

# Definir a instrução de sistema
sargento_instruction = """Você é um Sargento do Exército Brasileiro, da Seção de Comunicação Social e responsável por prestar informações para os cidadãos.
Você deve buscar informações no (google_search) relacionadas ao Serviço Militar Inicial Obrigatório ou voluntário na área da 9ª Região Militar e Comando Militar do Leste, utilizando, principalmente,
as informações contidas no site da 9ª Região Militar (https://9rm.eb.mil.br/), mas não se limitando a ele.
Além do Serviço Militar Inicial, também deve estar em condições de informar sobre Serviço Militar Voluntário, Alistamento, deveres do reservista e Exercício de Apresentação da Reserva (ExAR).
Também pode-se utilizar os sites do exército (https://www.eb.mil.br) e do Ministério da Defesa (https://www.gov.br/defesa/pt-br)
Algumas dúvidas mais específica, podem utilizar as seguintes legislações como fonte de consulta:
1 - LSM (https://www.planalto.gov.br/ccivil_03/LEIS/L4375.htm)
2 - RLSM (https://www.planalto.gov.br/ccivil_03/decreto/d57654.htm)
3 - Estatuto dos Militares (https://www.planalto.gov.br/ccivil_03/leis/l6880compilada.htm)
4 - Port 407 DGP(https://www.sgex.eb.mil.br/sg8/005_normas/01_normas_diversas/04_departamento-geral_do_pessoal/port_n_475_dgp_06dez2023.html)
5 - Port 2221 DGP (https://www.sgex.eb.mil.br/sg8/002_instrucoes_gerais_reguladoras/01_gerais/port_n_2221_cmdo_eb_01abr2024.html)
A forma de tratamento deve ser sempre polida e firma, podendo utilizar vocativos como \"combatente\", ou \"cidadão\".
Se a dúvida não tiver conexão com o Serviço Militar, devolva o seguinte resultado: 'O assunto não é pertinente ao Serviço Militar'.

 Você deve verificar as informações recebidas e deixá-las de forma sucinta
"""

# Configurar o modelo COM a instrução de sistema e então iniciar o chat
try:
    # Passamos system_instruction AQUI ao criar a instância do modelo
    model_instance = generativeai.GenerativeModel(
        model_name=modelo, # Nome do modelo
        system_instruction=sargento_instruction # INSTRUÇÃO DE SISTEMA VAI AQUI
        # Outras configurações de geração (como temperature, max_output_tokens, etc.) iriam aqui
        # Por exemplo: generation_config={'temperature': 0.7}
    )
    # Iniciamos o chat na instância do modelo já configurada
    chat = model_instance.start_chat()

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
        # Retorna erro 503 Service Unavailable se o chat não foi inicializado
        return jsonify({"response": "Erro interno: Chatbot não inicializado. Verifique os logs do servidor."}), 503

    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"response": "Por favor, envie uma mensagem."}), 400

    try:
        # Envia a mensagem para o modelo. O objeto chat gerencia o histórico.
        response = chat.send_message(user_message)

        # A resposta pode vir em diferentes formatos.
        # Tentamos acessar .text primeiro.
        try:
            bot_response = response.text
        except ValueError:
             # Se .text não estiver disponível (ex: resposta com tool_code),
             # você pode querer inspecionar response.parts, response.candidates, etc.
             # Para este exemplo simples, vamos apenas indicar que houve uma resposta não textual
             # e, idealmente, logar o conteúdo completo para depuração.
             bot_response = "Recebi uma resposta do modelo que não é puramente texto. Pode ser uma chamada de ferramenta. Por favor, tente outra pergunta ou verifique os logs do servidor."
             print("Aviso: Resposta do modelo não continha .text. Conteúdo completo da resposta:", response)
        except Exception as e:
             bot_response = f"Erro ao processar a resposta do modelo: {e}"
             print(f"Erro inesperado ao processar a resposta do modelo: {e}")


    except Exception as e:
        bot_response = f"Erro ao comunicar com o modelo: {e}" # Tratamento de erro se a chamada send_message falhar
        print(f"Erro durante o envio da mensagem ao modelo: {e}")

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    # Certifique-se de ter um arquivo .env com GOOGLE_API_KEY='SUA_CHAVE_API' na mesma pasta.
    # Execute com `python app.py` no terminal com o ambiente virtual ativado.
    app.run(debug=True)