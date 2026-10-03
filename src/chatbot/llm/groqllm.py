import os
from langchain_groq.chat_models import ChatGroq
import streamlit as st

class loadllm:
    def __init__(self, user_controls):
        self.user_controls =user_controls

    def loadingllm(self):
       
        try:
            if self.user_controls["selected_model_key"] == '': 
                st.error("Please enter the key")
                return
    
            llm = ChatGroq(api_key=self.user_controls["selected_model_key"],model = self.user_controls["selected_groq_model"])

        except Exception as e:
            raise ValueError(f"Error found ; {e}")
        return llm