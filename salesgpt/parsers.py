import re
from typing import Union

from langchain.agents.agent import AgentOutputParser
from langchain.agents.conversational.prompt import FORMAT_INSTRUCTIONS
from langchain.schema import AgentAction, AgentFinish  # OutputParserException


class SalesConvoOutputParser(AgentOutputParser):
    # Prefixo para identificar a fala do agente de vendas
    ai_prefix: str = "AI"  # altere para salesperson_name
    # Modo verboso para exibir informações de depuração
    verbose: bool = False

    def get_format_instructions(self) -> str:
        # Retorna as instruções de formatação do agente de vendas
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        # Se o modo verboso estiver ativado, exibe o texto de entrada
        if self.verbose:
            print("TEXT")
            print(text)
            print("-------")
        # Verifica se o texto contém o prefixo do agente de vendas
        if f"{self.ai_prefix}:" in text:
            # Retorna a ação do agente de vendas
            return AgentFinish(
                {"output": text.split(f"{self.ai_prefix}:")[-1].strip()}, text
            )
        # Expressão regular para extrair ação e entrada da ação
        regex = r"Action: (.*?)[\n]*Action Input: (.*)"
        match = re.search(regex, text)
        # Se não houver correspondência, retorna uma mensagem padrão
        if not match:
            return AgentFinish(
                {
                    "output": "Peço desculpas, não consegui encontrar a resposta para a sua pergunta. Posso ajudar com mais alguma coisa?"
                },
                text,
            )
        # Extrai a ação e a entrada da ação
        action = match.group(1)
        action_input = match.group(2)
        # Retorna a ação e a entrada da ação
        return AgentAction(action.strip(), action_input.strip(" ").strip('"'), text)

    @property
    def _type(self) -> str:
        # Retorna o tipo de agente (vendas)
        return "sales-agent"
