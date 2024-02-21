import json

from langchain_community.chat_models import ChatLiteLLM

from salesgpt.agents import SalesGPT

# Modelo GPT a ser utilizado
GPT_MODEL = "gpt-3.5-turbo-0613"
# GPT_MODEL_16K = "gpt-3.5-turbo-16k-0613"


class SalesGPTAPI:
    # Variável para determinar se as ferramentas serão usadas
    USE_TOOLS = True

    def __init__(self, llm, verbose=False):
        self.llm = llm
        self.verbose = verbose

    def do(self, conversation_history, human_input):
        # Lógica para processar a conversa e gerar a resposta
        # Retorna o nome do agente e a resposta
        return agent_name, agent_reply

    def get_initial_message(self):
        # Crie uma instância da classe SalesGPT
        sales_gpt = SalesGPT(config_path=self.config_path, verbose=self.verbose)
        # Faça com que o agente retorne a primeira mensagem
        name, reply = sales_gpt.do([], None)
        return name, reply

    def __init__(
        self, config_path: str, verbose: bool = False, max_num_turns: int = 100
    ):
        # Caminho para o arquivo de configuração do agente
        self.config_path = config_path
        # Ativação do modo verboso
        self.verbose = verbose
        # Número máximo de turnos na conversa de vendas
        self.max_num_turns = max_num_turns
        # Inicialização do modelo de linguagem
        self.llm = ChatLiteLLM(temperature=0.2, model_name=GPT_MODEL)

    def do(self, conversation_history: [str], human_input=None):
        # Verificação do arquivo de configuração do agente
        if self.config_path == "":
            print("No agent config specified, using a standard config")
            # Verificação do uso de ferramentas
            if self.USE_TOOLS:
                # Inicialização do agente de vendas com ferramentas
                sales_agent = SalesGPT.from_llm(
                    self.llm,
                    use_tools=True,
                    product_catalog="examples/perfil_product_catalog.txt",
                    salesperson_name="Leandro",
                    verbose=self.verbose,
                )
            else:
                # Inicialização do agente de vendas sem ferramentas
                sales_agent = SalesGPT.from_llm(self.llm, verbose=self.verbose)

        else:
            # Carregamento do arquivo de configuração do agente
            with open(self.config_path, "r") as f:
                config = json.load(f)
            # Verificação do modo verboso
            if self.verbose:
                print(f"Agent config {config}")
            # Inicialização do agente de vendas com base na configuração
            sales_agent = SalesGPT.from_llm(self.llm, verbose=self.verbose, **config)

        # Verificação do número máximo de turnos
        current_turns = len(conversation_history) + 1
        if current_turns >= self.max_num_turns:
            # Impressão de mensagem caso o número máximo de turnos seja atingido
            print("Maximum number of turns reached - ending the conversation.")
            return "<END_OF_>"

        # Inicialização do agente de vendas
        sales_agent.seed_agent()
        sales_agent.conversation_history = conversation_history

        # Verificação da entrada do usuário
        if human_input is not None:
            # Execução do passo do usuário
            sales_agent.human_step(human_input)

        # Execução do próximo passo da conversa
        sales_agent.step()

        # Verificação do término da conversa
        if "<END_OF_CALL>" in sales_agent.conversation_history[-1]:
            print("Sales Agent determined it is time to end the conversation.")
            return "<END_OF_CALL>"

        # Recuperação da última resposta do agente
        reply = sales_agent.conversation_history[-1]

        # Verificação do modo verboso
        if self.verbose:
            print("=" * 10)
            print(f"{sales_agent.salesperson_name}:{reply}")
        return reply.split(": ")
    
