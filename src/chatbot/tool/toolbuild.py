from langchain_community.tools.tavily_search import TavilySearchResults
from tavily import TavilyClient
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
#from langchain.tools.retriever import create_retriever_tool
#from langchain.agents import create_retriever_tool

from src.chatbot.rag.ragbuild import raginit

import streamlit as st

class toolinit:
    def __init__(self,user_controls):
        self.user_controls = user_controls


    def websearchtool(self):
        tavilytool = TavilySearchResults(max_result=1)
        return tavilytool


    def magicnumber(self,a:int,b:int)->int:
        """ get two integer inputs as a and b , return the magic number that is the sum of both"""
        return a+b

    def AINews(self,frequency:str)->dict:
        """ Fetch AI news based on specified frequency input of Daily, Monthly, Weekly
        Args: 
            frequency : Daily, Weekly , Monthly
        Returns:
            dict: updated news data for the given frequency
    
        """

        tavily=TavilyClient()
        time_range_map={'Daily':'d', 'Weekly':'w', 'Monthly':'m'}
        days_map={'Daily':1, 'Weekly':7, 'Monthly':30}

        response = tavily.search(
            query="Top Artificail Intelligence (AI) technology News India and Globally" ,
            topic="news",
            time_range= time_range_map[frequency],
            include_answer="advanced",
            max_result=15,
            days=days_map[frequency])

        return response.get('results',[])


    def ragtool(self,query: str)->str:
        """
        Tool: Retrieves relevant context for a query inputs asking for rag search.
        Always returns a string. 
        Never raises.
        """
        if not query:
            return "Empty query provided."


        #if "retriever" not in st.session_state:
        #    st.session_state.retriever = ragbuild()
 
        rag = raginit(self.user_controls)  
       
        retriever = rag.ragbuild()

        
        docs = retriever.invoke(query)
        return "\n\n".join(d.page_content for d in docs)

        # Return readable string
        #return "\n\n".join([d.page_content for d in docs])


#def ragtool():
#    retriever = ragbuild()
#    return create_retriever_tool(retriever,name="RAG_Tool",description="Search and retrieve information for RAG search")