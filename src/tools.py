from typing import Optional, Type, List
from pydantic import  Field
from pydantic import BaseModel
from langchain_core.tools import BaseTool
from langchain.agents import tool
import streamlit as st


class Params(BaseModel):
    regulatory_summary: dict = Field(description="Regulatory summaty ")
    impact_analysis: dict = Field(description="Impact Analysis")
    action_plan: dict = Field(description="Action plan ")
    final_recommendations: dict = Field(description="final recommendations ")

@tool(args_schema=Params)
def show_analisys_to_user(**document):
    """Use this action to show to the user the Regulatory Impact Analysis Document
    """
    st.session_state.document = document
    return "The document was shown with success."


tools=[show_analisys_to_user]