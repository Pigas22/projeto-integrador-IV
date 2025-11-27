#from google import genai
from google import genai
from dotenv import load_dotenv
import os

PROMPT = """
Você é um asssistente virtual de um centro hospitalar.
Seu objetivo é ajudar os pacientes a agendar consultas, fornecer informações sobre serviços médicos e responder a dúvidas comuns relacionadas à saúde.
Seja educado, profissional e empático em suas respostas.
Além disso, tente sempre direcionar os pacientes para os recursos apropriados do hospital quando necessário. Não tire conclusões médicas ou forneça diagnósticos, apenas oriente os pacientes a procurar um profissional de saúde qualificado para avaliações médicas.
Seja claro e conciso em suas respostas, evitando jargões médicos complexos que possam confundir os pacientes.
"""

API_KEY = os.getenv("CHATBOT_API_KEY")

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def run_chatbot_with_prompt(initial_prompt: str):
    """
    Inicializa o chatbot lendo a chave do .env e inicia a conversa
    com um prompt inicial.
    """
    
    # 2. O SDK do Gemini (genai.Client()) busca a chave
    #    automaticamente da variável de ambiente GEMINI_API_KEY.
    #    A função load_dotenv() garante que ela está carregada.
    try:
        # Se a chave não for encontrada, o construtor do cliente pode falhar
        # ou emitir um aviso, dependendo da versão do SDK e da configuração.
        # Geralmente, se o .env estiver correto, ele funciona sem passar nada aqui.
        client = genai.Client(api_key=API_KEY)
        
    except Exception as e:
        # Verifica se a variável de ambiente foi carregada
        if not API_KEY:
            print("ERRO: A variável GEMINI_API_KEY não foi encontrada. Verifique seu arquivo .env.")
        else:
            print(f"Erro ao inicializar o cliente Gemini: {e}")
        return

    # 3. Cria uma sessão de chat para manter o contexto
    #    do histórico da conversa
    chat = client.chats.create(model="gemini-2.5-flash-lite")

    print(f"🤖 Chatbot Gemini: Olá! Sou um chatbot alimentado por Gemini.")
    print("-" * 50)
    
    # 4. Envia o prompt inicial para o bot
    print(f"Você (Prompt Inicial): {initial_prompt}")
    
    try:
        response = chat.send_message(initial_prompt)
        print(f"🤖 Chatbot Gemini: {response.text}")
    except Exception as e:
        print(f"Ocorreu um erro ao gerar a primeira resposta: {e}")
        return

    print("-" * 50)
    print("Continue a conversa (digite 'sair' para encerrar):")

    # 5. Loop principal para continuar o chat
    while True:
        user_input = input("Você: ")

        if user_input.lower() in ["sair", "quit", "exit"]:
            print("🤖 Chatbot Gemini: Até logo! Foi um prazer conversar com você.")
            break

        if not user_input.strip():
            continue

        try:
            response = chat.send_message(user_input)
            print(f"🤖 Chatbot Gemini: {response.text}")
            
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break


if __name__ == "__main__":
    print("API is running...")
    run_chatbot_with_prompt(PROMPT)
