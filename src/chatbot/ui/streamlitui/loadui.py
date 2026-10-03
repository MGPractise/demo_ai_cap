import streamlit as st
import os

from src.chatbot.ui.streamlitui.uiconfigfile import config

class loadstreamui:
    def __init__(self):
        self.config = config()
        self.user_controls ={}


    def buildstreamui(self):
        st.set_page_config(page_title = "🤖 " + self.config.get_page_title_option(), layout ="wide")
        st.header( "💬 " + self.config.get_page_title_option() + " ⚡")
        st.caption('------------------------------------Live demo by MG---------------------------------------------')
        st.session_state.isnewsbuttonclicked = False
        st.session_state.url = ""

        with st.sidebar:

            self.user_controls["selected_llm"] = st.selectbox("Select LLM",self.config.get_llm_option())

            if self.user_controls["selected_llm"] == 'Groq':
                self.user_controls["selected_groq_model"] = st.selectbox("Select GROQ Model",self.config.get_groq_model_option())
                os.environ["GROQ_API_KEY"]=self.user_controls["selected_model_key"] = st.session_state["selected_model_key"] = st.text_input("API Key", type ="password")

                if not self.user_controls["selected_model_key"]:
                    st.warning("please enter the key")
            

            self.user_controls["selected_usecase"] = st.selectbox("Select UseCase",self.config.get_usecase_option())

            if self.user_controls["selected_usecase"] == 'Web Search Tool' or self.user_controls["selected_usecase"] == 'AI News':
                os.environ["TAVILY_API_KEY"]=self.user_controls["selected_web_key"] = st.session_state["selected_web_key"] = st.text_input("Web Key", type ="password")

                if not self.user_controls["selected_web_key"]:
                    st.warning("please enter the web key")
            
            if self.user_controls["selected_usecase"] == 'AI News':
                st.subheader("AI NEWS FREQUENCY")
                self.user_controls["selected_news_frequency"] = st.selectbox("Select New Frequency",self.config.get_news_option())

                if st.button("Fetch News"):
                    st.session_state.isnewsbuttonclicked = True

            if self.user_controls["selected_usecase"] == 'RAG':
                self.user_controls["selected_web_url"] = st.text_input("Web URL",key="selected_url")
                st.session_state.url = self.user_controls["selected_web_url"]
                st.write("OR")
                self.user_controls["uploaded_file"] = st.file_uploader("Upload file", type=["txt"])
                
                if self.user_controls["uploaded_file"] is not None:
                    st.write("File uploaded:", self.user_controls["uploaded_file"].name)

                if not self.user_controls["selected_web_url"] and not self.user_controls["uploaded_file"]:
                    st.warning("please enter URL or upload file")



            if self.user_controls["selected_usecase"] == 'SQL Query':
                self.user_controls["Instructions"] = st.text_area("Enter SQL Instructions",height=20,max_chars=500)

            if self.user_controls["selected_usecase"] == 'Knowledge Graph RAG':
                self.user_controls["graph_instructions"] = st.text_area("Enter Graph Instructions",height=20,max_chars=500)
        return self.user_controls




