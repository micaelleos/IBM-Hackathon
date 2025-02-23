
import os
import requests
import logging
from docling.document_converter import DocumentConverter
from langchain_ibm import WatsonxLLM, ChatWatsonx
from langchain_core.prompts import PromptTemplate

from langchain_community.llms import Replicate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from ibm_granite_community.notebook_utils import get_env_var
from langchain.tools.render import render_text_description_and_args
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv
import streamlit as st
from src.tools import tools
from src.prompts import system_prompt, human_prompt, assistant


load_dotenv()

@st.cache_resource()
def memory(id):
    memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")
    return memory

class ComplianceAgent:
    def __init__(self, params, regulation,hash):
        self.params =  params
        self.regulation = regulation
        self.ibm_cloud_api_key = get_env_var('WATSONX_APIKEY')
        self.project_id = get_env_var('WATSONX_PROJECT_ID')
        self.watson_url = get_env_var('WATSONX_URL')

        self.watson_llm = WatsonxLLM(
            model_id="ibm/granite-3-8b-instruct",
            apikey=self.ibm_cloud_api_key,
            project_id=self.project_id,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 2000,
                "min_new_tokens": 1,
                "repetition_penalty": 1,
                "temperature":0.8,
                "stop_sequences" : ["END","Observation:","PAUSE"]
            },
            url=self.watson_url,
        )

        self.tools = tools
        self.memory = memory(hash)


        # Defining Prompts
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", human_prompt),
                ("assistant",assistant)
            ]
        )

        self.prompt = self.prompt.partial(
            tools=render_text_description_and_args(list(tools)),
            tool_names=", ".join([t.name for t in tools]),
            regulation=regulation,
        )

        #Defining chain
        self.chain = (
            RunnablePassthrough.assign(
                agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
                chat_history=lambda x: self.memory.chat_memory.messages,
            )
            | self.prompt
            | self.watson_llm
            | JSONAgentOutputParser()
        )

        self.agent_executor = AgentExecutor(
            agent=self.chain, tools=self.tools, handle_parsing_errors=True, verbose=True, memory=self.memory, max_iterations= 3
        )

    def chat(self,query):    
        response=self.agent_executor.invoke({'input':query})
        return response['output']