from typing import Callable

from langchain.prompts.base import StringPromptTemplate


class CustomPromptTemplateForTools(StringPromptTemplate):
    # O template a ser utilizado
    template: str
    ############## NOVO ######################
    # O método para obter a lista de ferramentas disponíveis
    tools_getter: Callable

    def format(self, **kwargs) -> str:
        # Obtém os passos intermediários (tuplas AgentAction, Observation)
        # Formata-os de uma maneira específica
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Define a variável agent_scratchpad com esse valor
        kwargs["agent_scratchpad"] = thoughts
        ############## NOVO ######################
        # Obtém a lista de ferramentas utilizando o método fornecido
        tools = self.tools_getter(kwargs["input"])
        # Cria uma variável 'tools' a partir da lista de ferramentas fornecidas
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in tools]
        )
        # Cria uma lista de nomes de ferramentas para as ferramentas fornecidas
        kwargs["tool_names"] = ", ".join([tool.name for tool in tools])
        # Retorna o template formatado com as variáveis substituídas
        return self.template.format(**kwargs)
