# Alura-Gemini
Desafio do Imersão Alura - Google Gemini

Obs: Se baixar somente o arquivo Sargento_Bot.ipynb e importar para o Colab, será possível testar.
Utilizando o Google Studio AI, solicitei para criar uma interface html para ficar mais acessível e amigável. Testei no Visual Studio Code e "na minha máquina funcionou" 😆

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
    git clone https://github.com/bogado85
    cd Alura-Gemini
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

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
