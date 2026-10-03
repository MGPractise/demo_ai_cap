import streamlit as st

from src.chatbot.ui.streamlitui.loadui import loadstreamui

from src.chatbot.llm.groqllm import loadllm

from src.chatbot.graph.graphbuild import graphbuild

from src.chatbot.ui.streamlitui.displayui import displayresult

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


def loadchatbot():

    """
    Loads and run langraph agenticai application with streamlit UI.
    """

    ls = loadstreamui()
    user_controls = ls.buildstreamui()

    if not user_controls:
        st.error("Failed to load controls")
        return


    user_query = st.chat_input ("type the chat input")

    if user_query or st.session_state.isnewsbuttonclicked:


        loadmodel = loadllm(user_controls)
        llm = loadmodel.loadingllm()

        if not llm:
            st.error("Failed to load model")
            return


        loadgraph = graphbuild(llm,user_controls)

        if not loadgraph:
            st.error("Failed to load graph")
            return

        if user_controls["selected_usecase"] == 'AI News':
            user_query = HumanMessage(content=user_controls["selected_news_frequency"] + "News") 

        if user_controls["selected_usecase"] == 'RAG':
            user_query =  "RAG Seach on " + user_query

        try:
            graph = loadgraph.graphsetup(user_controls["selected_usecase"])
            displayresult(user_controls["selected_usecase"],graph,user_query).displayresultui()
        except Exception as e:
            st.error(f" Failed to load aa{e}")
            return

    
 




