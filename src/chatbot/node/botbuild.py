from src.chatbot.state.statebuild import state
from src.chatbot.state.routebuild import route
from src.chatbot.tool.toolbuild import toolinit
#websearchtool, magicnumber, AINews, ragtool
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

import os
from sqlalchemy import create_engine, text
from langchain_neo4j import Neo4jGraph
import re






class botbuild:
    def __init__(self,model,user_controls ):
        self.llm = model
        self.user_controls  = user_controls 
        self.toolinit = toolinit(user_controls)


    def basicbot(self, state:state)->dict:
        return {"messages" : self.llm.invoke(state['messages'])}


    def toolbot(self, state:state)->dict:
        """Provide answer to queries on websearchtool, magicnumber, AINews """
        tools = [self.toolinit.websearchtool(), self.toolinit.magicnumber, self.toolinit.AINews]
        llmtool=self.llm.bind_tools(tools)
        return {"messages" : llmtool.invoke(state['messages'])}
    
    def tools(self):
        tools = [self.toolinit.websearchtool(), self.toolinit.magicnumber, self.toolinit.AINews]
        return ToolNode(tools)

    def ragbot(self, state:state)->dict:
        tools = [self.toolinit.ragtool]
        llmtool=self.llm.bind_tools(tools)
        return {"messages" : llmtool.invoke(state['messages'])}
    
    def ragtools(self):
        tools = [self.toolinit.ragtool]
        return ToolNode(tools)

    def summarize(self, state:state)->dict:
        """ Summarize input data
        Args: 
            state : containing raw information

        Return:
            dict: updated state with summary information
        """

        if self.user_controls["selected_usecase"] == "SQL Query" or self.user_controls["selected_usecase"] == "Knowledge Graph RAG":
            promp_template = ChatPromptTemplate.from_messages([
                ("system",""" You are a professional summarization agent.
                Task:
                Summarize the content below in a structured format.

                Instructions:
                - Be concise and factual
                - Avoid repetition
                - Do not add new information



                Output Format:
                - **Overview**
                - **Cypher or SQL Query**: show input query only if available 
                - **Cypher or SQL Output**: show query output in table only if available
                - **Key Points**: bullet list
                """),
                ("user","Content:\n{content}")])
        else:
            promp_template = ChatPromptTemplate.from_messages([
                ("system",""" You are a professional summarization agent.
                Task:
                Summarize the content below in a structured format.

                Instructions:
                - Be concise and factual
                - Avoid repetition
                - Do not add new information

                Output Format:
                - **Overview**
                - **Key Points**: bullet list with url link if url is available in input
                """),
                ("user","Content:\n{content}")])

        content_blocks = []

        for msg in state["messages"]:
            if isinstance(msg, (HumanMessage,AIMessage)) and msg.content:
                content_blocks.append(msg.content)

        combined_text = "\n".join(content_blocks)

        
        summary = self.llm.invoke(promp_template.format(content=combined_text))

       
        summary_msg = AIMessage(content=summary.content)
        return {"messages": [summary_msg]}
    

    def routing(self, state:state)->dict:
        """ Give the route to the next node
        """

        routellm = self.llm.with_structured_output(route)

        promp_template = ChatPromptTemplate.from_messages([
                    (
            "system",
            """
            You are an intent router for an AI system.

            Decide the next step:
            - "sql" → when the question requires querying a database
            - "tool" → when the question requires reasoning, RAG, search, or explanation

            Route to "sql" if the user asks for:
            - totals, counts, sums, averages
            - lists or filters of stored data
            - grouping, aggregation, joins
            - questions like: how many, total, list, show

            Examples:
            "total quantity sold" → sql
            "list all users" → sql
            "show orders per user" → sql

            "what is SQL" → tool
            "explain langgraph" → tool
            "search postgres tutorial" → tool

            Return ONLY the step.
            """
                    ),
                    ("user", "{content}")
                ])



        
        summary = routellm.invoke(promp_template.format(content=state["messages"]))
        print(summary.step)
        return {"step": summary.step}

    
    def routedecision(self,state:state)->dict:
        return state["step"]

    def sqlquery(self, state:state)->dict:
        """For data analytics related questions provides the answer using SQL query and database data """

        DATABASE_URL = 'postgresql://neondb_owner:npg_HD8hVzRk9GMm@ep-restless-field-a8mlstkb-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require'

        engine = create_engine(DATABASE_URL,pool_pre_ping=True)

        schema = {}

        query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """

        with engine.connect() as conn:
            rows = conn.execute(text(query)).fetchall()

        for table, column, dtype in rows:
            schema.setdefault(table, []).append(f"{column} ({dtype})")


        schema_text = "\n".join(
        f"{table}: {', '.join(cols)}"
        for table, cols in schema.items())

        

        print (schema_text)
        prompt = f"""
        You are a PostgreSQL expert.

        Use ONLY this schema:
        {schema_text}

        User question:
        {state['messages']}

        Rules:
        - Only SELECT queries
        - Use correct table & column names
        - Add LIMIT 100
        - Return ONLY SQL CODE
        - {self.user_controls["Instructions"]}
        """

        sql_query = self.llm.invoke(prompt).content.strip().lower()
        print(sql_query)

        if sql_query.startswith("```"):
            
            sql_query = "\n".join(sql_query.split("\n")[1:-1])
        
        #if any(word in sql for word in forbidden):
        #   return {**state, "error": "Unsafe SQL detected"}

        try:
            with engine.connect() as conn:
                result = conn.execute(text(sql_query))
                rows = [dict(row._mapping) for row in result.fetchall()]
                
            return {"messages":[{"role": "assistant","content": "input query -" + sql_query + "Query Output -" + str(rows)}]}
        except Exception as e:
            return {"messages": e}

    


    def graphquery(self, state:state)->dict:
        """For data analytics related questions provides the answer using cypher query and graph database data """

        NEO4J_URI = "neo4j+s://1e770572.databases.neo4j.io"
        NEO4J_USERNAME = "1e770572"
        NEO4J_PASSWORD = "cH84hFjJDDS0dRF8YezS6X_D8ZIeDGE2kAqTN6X0yJI"
        NEO4J_DATABASE = "1e770572"

        graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        database = NEO4J_DATABASE
)

        schema_text = graph.get_schema
        print("Schema:\n", schema_text)

        prompt = f"""
        You are a Cypher expert.

        Use ONLY this schema:
        {schema_text}

        User question:
        {state['messages']}

        Rules:
        - Only data retrieval queries (MATCH / RETURN only)
        - Use exact case-sensitive node labels and relationship names from the schema
        - Return ONLY executable Cypher code without markdown explanations or code blocks
        - {self.user_controls.get("graph_instructions", "")}
        """

        # 2. Invoke LLM and keep case-sensitivity (remove .lower())
        raw_response = self.llm.invoke(prompt).content.strip()

        # 3. Safe regex markdown block cleanup
        cypher_query = re.sub(r"```(?:cypher)?", "", raw_response).replace("```", "").strip()
        print("Generated Cypher:", cypher_query)

        try:
            # 4. graph.query directly returns a list of dictionaries
            rows = graph.query(cypher_query)

            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": f"Input Query: {cypher_query}\nQuery Output: {rows}",
                    }
                ]
            }
        except Exception as e:
            # 5. Return properly formatted error state
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": f"Failed to execute Cypher query: {str(e)}",
                    }
                ]
            }