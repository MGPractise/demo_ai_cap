from langgraph.graph import StateGraph, START, END

from src.chatbot.state.statebuild import state

from src.chatbot.node.botbuild import botbuild

from src.chatbot.tool.toolbuild import toolinit

from langgraph.prebuilt import ToolNode, tools_condition

class graphbuild:
    def __init__(self, llm,user_controls):
        self.llm= llm
        self.user_controls = user_controls
        self.graph = StateGraph(state)

    def basichatbot(self):
        botnode = botbuild(self.llm,self.user_controls )
        self.graph.add_node("basicbot",botnode.basicbot)
        self.graph.add_edge(START, "basicbot")
        self.graph.add_edge("basicbot", END)

    def toolchatbot(self):
        botnode = botbuild(self.llm,self.user_controls )
        tools = botnode.tools()
        self.graph.add_node("toolbot",botnode.toolbot)
        self.graph.add_node("tools",tools)
        self.graph.add_node("summarize",botnode.summarize)
        self.graph.add_edge(START, "toolbot")
        self.graph.add_conditional_edges("toolbot", tools_condition)
        #self.graph.add_edge("tools", END)
        self.graph.add_edge("tools", "toolbot")        
        #self.graph.add_edge("toolbot", END) 
        self.graph.add_edge("toolbot", "summarize")
        self.graph.add_edge("summarize", END)

    def ragchatbot(self):
        botnode = botbuild(self.llm,self.user_controls)
        tools = botnode.ragtools()
        #tools.max_calls = 2
        self.graph.add_node("toolbot",botnode.ragbot)
        self.graph.add_node("tools",tools)
        self.graph.add_node("summarize",botnode.summarize)
        self.graph.add_edge(START, "toolbot")
        self.graph.add_conditional_edges("toolbot", tools_condition)
        #self.graph.add_edge("tools", END)
        #self.graph.add_edge("tools", "toolbot")        
        #self.graph.add_edge("toolbot", END) 
        self.graph.add_edge("tools", "summarize")
        #self.graph.add_edge("toolbot", "summarize")
        self.graph.add_edge("summarize", END)

    def sqlchatbot(self):
        botnode = botbuild(self.llm,self.user_controls )
        #tools = botnode.tools()
        #self.graph.add_node("toolbot",botnode.toolbot)
        #self.graph.add_node("tools",tools)
        self.graph.add_node("summarize",botnode.summarize)
        #self.graph.add_node("routing",botnode.routing)
        self.graph.add_node("sqlquery",botnode.sqlquery)
        #self.graph.add_edge(START, "routing")
        self.graph.add_edge(START, "sqlquery")
        #self.graph.add_conditional_edges("routing", botnode.routedecision,{"tool":"toolbot","sql":"sqlquery"})
        self.graph.add_edge("sqlquery", "summarize")
        #self.graph.add_conditional_edges("toolbot", tools_condition)
        #self.graph.add_edge("tools", END)
        #self.graph.add_edge("tools", "toolbot")        
        #self.graph.add_edge("toolbot", END) 
        #self.graph.add_edge("toolbot", "summarize")
        self.graph.add_edge("summarize", END)

    def graphchatbot(self):
        botnode = botbuild(self.llm,self.user_controls )
        #tools = botnode.tools()
        #self.graph.add_node("toolbot",botnode.toolbot)
        #self.graph.add_node("tools",tools)
        self.graph.add_node("summarize",botnode.summarize)
        #self.graph.add_node("routing",botnode.routing)
        self.graph.add_node("graphquery",botnode.graphquery)
        #self.graph.add_edge(START, "routing")
        self.graph.add_edge(START, "graphquery")
        #self.graph.add_conditional_edges("routing", botnode.routedecision,{"tool":"toolbot","sql":"sqlquery"})
        self.graph.add_edge("graphquery", "summarize")
        #self.graph.add_conditional_edges("toolbot", tools_condition)
        #self.graph.add_edge("tools", END)
        #self.graph.add_edge("tools", "toolbot")        
        #self.graph.add_edge("toolbot", END) 
        #self.graph.add_edge("toolbot", "summarize")
        self.graph.add_edge("summarize", END)




    
    def graphsetup(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basichatbot()
        elif usecase == "Web Search Tool" or usecase == "AI News":
            self.toolchatbot()
        elif usecase == "SQL Query":
            self.sqlchatbot()
        elif usecase == "RAG":
            self.ragchatbot()
        elif usecase == "Knowledge Graph RAG":
            self.graphchatbot()
        
        
        return self.graph.compile()


