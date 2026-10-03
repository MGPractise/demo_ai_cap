import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json


class displayresult:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message =user_message
     
    def displayresultui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        if usecase == "Basic Chatbot" :
            for event in graph.stream({'messages':("user",user_message)}):
                print(event.values())
                for value in event.values():
                    print(value['messages'])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)

        elif usecase == "Web Search Tool" or usecase == "AI News" or usecase == "RAG" or usecase == "SQL Query" or usecase == "Knowledge Graph RAG" : 
            
            with st.spinner("Chatbot is thinking ⏳"):
                initial_state={"messages": [user_message]}
                res = graph.invoke(initial_state)
                tool_call_map = {}



            for message in res["messages"]:
                if type(message)== AIMessage and message.content:
                    last_AIMessage = message.content
                if isinstance(message, AIMessage) and message.tool_calls:
                    for call in message.tool_calls:
                        tool_call_map[call["id"]] = call["name"]
            for message in res['messages']:
                if type(message)== HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message)== ToolMessage:
                    tool_name = tool_call_map.get(message.tool_call_id, "Unknown Tool")
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.markdown(f"🛠 **Tool Called:** `{tool_name}`")
                        st.write(message.content)
                        st.write("Tool Call End")
                #elif type(message)== AIMessage and message.content:
                    #with st.chat_message("assistant"):   
                        #st.write(message.content)
             #elif type(message)== AIMessage and message.content:
            if  last_AIMessage:
                with st.chat_message("assistant"):   
                    st.write(last_AIMessage)          
        
        elif usecase == "Web Search Tool2":
            for event in graph.stream({"messages": [HumanMessage(content=user_message)]}):
                for value in event.values():
                    for msg in value["messages"]:

                        # USER
                        if isinstance(msg, HumanMessage):
                            with st.chat_message("user"):
                                st.write(msg.content)

                        # LLM
                        elif isinstance(msg, AIMessage):
                            with st.chat_message("assistant"):
                                st.write(msg.content)

                        # TOOL
                        elif isinstance(msg, ToolMessage):
                            with st.chat_message("assistant"):
                                st.markdown("🛠 **Tool Output**")
                                st.write(msg.content)

