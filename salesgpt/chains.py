# Importa as classes e módulos necessários
from langchain.chains import LLMChain  # Importa a classe LLMChain
from langchain.prompts import PromptTemplate  # Importa a classe PromptTemplate
from langchain_community.chat_models import ChatLiteLLM  # Importa a classe ChatLiteLLM

from salesgpt.logger import time_logger  # Importa a função time_logger
from salesgpt.prompts import (  # Importa as constantes de prompts
    SALES_AGENT_INCEPTION_PROMPT,
    STAGE_ANALYZER_INCEPTION_PROMPT,
)


class StageAnalyzerChain(LLMChain):
    """Classe para analisar em qual estágio da conversa a conversa deve avançar."""

    @classmethod
    @time_logger  # Decoração para registrar o tempo de execução
    def from_llm(cls, llm: ChatLiteLLM, verbose: bool = True) -> LLMChain:
        """Obtém o analisador de resposta."""
        # Define o prompt inicial para o analisador de estágio
        stage_analyzer_inception_prompt_template = STAGE_ANALYZER_INCEPTION_PROMPT
        # Cria um template de prompt com as variáveis de entrada necessárias
        prompt = PromptTemplate(
            template=stage_analyzer_inception_prompt_template,
            input_variables=[
                "conversation_history",
                "conversation_stage_id",
                "conversation_stages",
            ],
        )
        # Retorna uma instância da classe StageAnalyzerChain com o prompt e o modelo de chat especificados
        return cls(prompt=prompt, llm=llm, verbose=verbose)


class SalesConversationChain(LLMChain):
    """Classe para gerar a próxima declaração para a conversa."""

    @classmethod
    @time_logger  # Decoração para registrar o tempo de execução
    def from_llm(
        cls,
        llm: ChatLiteLLM,
        verbose: bool = True,
        use_custom_prompt: bool = False,
        custom_prompt: str = "You are an AI Sales agent, sell me this pencil",
    ) -> LLMChain:
        """Obtém o analisador de resposta."""
        # Verifica se deve usar um prompt personalizado
        if use_custom_prompt:
            sales_agent_inception_prompt = custom_prompt
        else:
            sales_agent_inception_prompt = SALES_AGENT_INCEPTION_PROMPT
        # Cria um template de prompt com as variáveis de entrada necessárias
        prompt = PromptTemplate(
            template=sales_agent_inception_prompt,
            input_variables=[
                "salesperson_name",
                "salesperson_role",
                "company_name",
                "company_business",
                "company_values",
                "conversation_purpose",
                "conversation_type",
                "conversation_history",
            ],
        )
        # Retorna uma instância da classe SalesConversationChain com o prompt e o modelo de chat especificados
        return cls(prompt=prompt, llm=llm, verbose=verbose)
