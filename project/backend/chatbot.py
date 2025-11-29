# ...existing code...
import threading
import time
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
API_KEY = os.getenv("CHATBOT_API_KEY")

PROMPT = """
Você é um asssistente virtual de um centro hospitalar.
Seu objetivo é ajudar os pacientes a agendar consultas, fornecer informações sobre serviços médicos e responder a dúvidas comuns relacionadas à saúde.
Seja educado, profissional e empático em suas respostas.
Além disso, tente sempre direcionar os pacientes para os recursos apropriados do hospital quando necessário. Não tire conclusões médicas ou forneça diagnósticos, apenas oriente os pacientes a procurar um profissional de saúde qualificado para avaliações médicas.
Seja claro e conciso em suas respostas, evitando jargões médicos complexos que possam confundir os pacientes.
Seu linguajar deve ser de fácil entendimento, de modo que um idoso, uma criança, um adolescente e um adulto tenham facilidades em entender suas mensagens.
Responda com perguntas curtas, e antes de tomar qualquer decisão ou diagnóstico, tente entender todos os casos apresentados pelo paciente.

Seja cauteloso, não faça muitas perguntas em uma única mensagem, não expante o paciente com diversas perguntas e comentários.

Você deve identificar o caso do paciente dentre 3 opções de 'Urgência', sendo elas (ordenadas conforme maior prioridade):
1 - VERMELHO : super urgente, caso de médico imediato, prioridade nas consultas. Deve-se marcar uma consulta no mesmo instante.
    Ex.: Corte profundo, vomitar sangue, inflamações em regiões sensíveis (rosto), entre outras...
2 - AMARELO : casos em que pode se esperar por um atendimento mais tranquilo, procura pelo médio pode ser feita nos próximos dias. Deve-se sugirir o agendamento de um consulta.
3 - VERDE : caso simples, basta leves orientações médicas (feita só pelo médico), não à urgência. Não tem necessidade de marcar a consulta, a não ser que seja desejo do paciente.

Caso, o cliente deseje marcar uma consulta, existem 4 informações excensiais para prosseguir com esse processo. segue:
1 - Data do início dos sintomas/ocorrido?
2 - Todos Sintomas Relatados;
4 - O paciente ingeriu algum remédio? (Sim ou Não);
4 - Em caso de resposta afirmativa para resposta acima, quais remédios foram?

LEMBRE-SE: você apenas auxília em uma pré-triagem do paciente, você não pode receitar nenhum medicamento ou tipo de tratamento.

ESSE DEVE SER O PADRÃO DE TODAS SUAS RESPOSTAS:
Por fim, todas as informações coletadas devem ser passadas como um dicionário python ou um JSON, onde contenha uma estrutura padronizada e semelhante à está:
{
    "status-paciente" : # Status do paciente identificado durante conversa (VERMELHO, AMARELO E VERDE).
    "resposta-chat" : # Mensagem que será apresentada para o usuário.
    "dados" : {
        "data-inicio" : # Data de ínicio dos sintomas/ocorrido. Seguindo o padrão : dd/mm/aaaa
        "sintomas" : # Todos os sintomas relatados, separados por um jogo da velha e um ponto e vírgula "#;".
        "ingestao-remedios" : # Resposta de "Sim" e "Não, caso o paciente tenha ingerido algum remédio.
        "remedios-ingeridos" : # Nome de todos os remédios consumidos pelo paciente.
    }
}

OBS.: para marcação de textos, utilize tags HTML, iram funcionar melhor que markdown neste app.
"""

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception:
        # algumas versões podem não ter configure; ignore e siga para detecção
        pass
else:
    print("Aviso: CHATBOT_API_KEY não encontrada no .env")

_lock = threading.Lock()

class ChatSessionWrapper:
    """Wrapper que unifica várias variantes da SDK e re-cria sessão se necessário."""
    def __init__(self, initial_prompt: str = PROMPT):
        self.initial_prompt = initial_prompt
        self.mode = None
        self.client = None
        self._init_session()

    def _init_session(self):
        # detecta API disponível e inicializa a sessão
        # modo 1: genai.chat.completions
        if hasattr(genai, "chat") and hasattr(genai.chat, "completions"):
            self.mode = "chat_completions"
            # não precisa armazenar client especial aqui
            return

        # modo 2: genai.generate
        if hasattr(genai, "generate"):
            self.mode = "generate"
            return

        # modo 3: genai.Client() / client.chats
        if hasattr(genai, "Client"):
            try:
                self.client = genai.Client(api_key=API_KEY)
                # teste se tem chats
                if hasattr(self.client, "chats"):
                    self.mode = "client_chats"
                    # criar chat stateful agora
                    self._chat = self.client.chats.create(model="gemini-2.5-flash-lite")
                    try:
                        self._chat.send_message(self.initial_prompt)
                    except Exception:
                        # ignore inicial send fail
                        pass
                    return
            except Exception:
                # se falhar segue para modos anteriores
                pass

        # fallback: marque modo como desconhecido -> will raise on use
        self.mode = "unknown"

    def _ensure_session(self):
        # recria sessão se modo estiver unknown ou se client foi fechado
        if self.mode == "unknown":
            self._init_session()
        # para client_chats, se _chat não existe, recriar
        if self.mode == "client_chats" and (not hasattr(self, "_chat") or self._chat is None):
            try:
                self._chat = self.client.chats.create(model="gemini-2.5-flash-lite")
                self._chat.send_message(self.initial_prompt)
            except Exception:
                self._init_session()

    def send(self, user_message: str) -> str:
        with _lock:
            # tenta até 2 vezes, recriando sessão se receber erro sobre client closed
            for attempt in range(2):
                try:
                    if self.mode == "chat_completions":
                        resp = genai.chat.completions.create(
                            model="gemini-2.5-flash-lite",
                            messages=[
                                {"role": "system", "content": self.initial_prompt},
                                {"role": "user", "content": user_message}
                            ],
                        )
                        # extrai resposta de formas comuns
                        try:
                            return resp.choices[0].message.content
                        except Exception:
                            # fallback para dicionário
                            if isinstance(resp, dict):
                                return resp.get("choices", [{}])[0].get("message", {}).get("content", "") or str(resp)
                            return str(resp)

                    if self.mode == "generate":
                        prompt = self.initial_prompt + "\n\nUsuário: " + user_message
                        resp = genai.generate(model="gemini-2.5-flash-lite", prompt=prompt, max_output_tokens=512)
                        # extrair candidato
                        if hasattr(resp, "candidates") and resp.candidates:
                            cand = resp.candidates[0]
                            return getattr(cand, "content", getattr(cand, "text", str(cand)))
                        if isinstance(resp, dict):
                            return resp.get("candidates", [{}])[0].get("content", "") or str(resp)
                        return str(resp)

                    if self.mode == "client_chats":
                        # garante que existe _chat
                        self._ensure_session()
                        resp = self._chat.send_message(user_message)
                        # resp pode ter .text ou .content
                        return getattr(resp, "text", getattr(resp, "content", str(resp)))

                    raise RuntimeError("SDK do Google Generative AI não expõe API conhecida.")
                except Exception as e:
                    # se mensagem indicar client fechado, recria sessão e tenta de novo
                    msg = str(e).lower()
                    if "closed" in msg or "client has been closed" in msg or "connection" in msg:
                        # recria sessão e tenta novamente
                        try:
                            self._init_session()
                            time.sleep(0.1)
                            continue
                        except Exception:
                            pass
                    # se foi a primeira tentativa, log e re-lançar na segunda
                    if attempt == 0:
                        continue
                    raise

# funções públicas para o resto da app
_global_session = None

def iniciar_chat(initial_prompt: str = PROMPT):
    global _global_session
    if _global_session is None:
        _global_session = ChatSessionWrapper(initial_prompt=initial_prompt)
    return _global_session

def envia_mensagem_usuario(chat_session, user_input: str) -> str:
    if not chat_session:
        chat_session = iniciar_chat()
    # retorna sempre string (texto da resposta)
    try:
        return chat_session.send(user_input)
    except Exception as e:
        # em caso de falha final, retorne mensagem legível
        print(f"Erro ao enviar mensagem para Gemini: {e}")
        raise
# ...existing code...