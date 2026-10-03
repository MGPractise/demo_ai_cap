from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, PDFMinerLoader, UnstructuredWordDocumentLoader


class raginit:
    def __init__(self,user_controls):
        self.user_controls= user_controls

    def ragbuild(self):
        

        #if "rag_retriever" not in st.session_state:

        if self.user_controls["uploaded_file"]:

            uploaded_file = self.user_controls["uploaded_file"]

            if uploaded_file.name.endswith(".txt"):
                content = uploaded_file.read().decode("utf-8")

                docs = [
                    Document(
                        page_content=content,
                        metadata={"source": uploaded_file.name})]

            #file = self.user_controls["uploaded_file"]

            #if file.name.endswith(".txt"):
                #loader = TextLoader(file)
            #elif file.name.endswith(".pdf"):
                #loader = PDFMinerLoader(file)
            #elif file.name.endswith(".docx"):
                #loader = UnstructuredWordDocumentLoader(file)
            #else:
                #st.error("Unsupported file type")

                doc_list = docs

        elif self.user_controls["selected_web_url"]:
            url = self.user_controls["selected_web_url"]
            print(url)
            docs = WebBaseLoader(url).load()
            doc_list = [item for item in docs]


        

        text_splitter = RecursiveCharacterTextSplitter(chunk_size =1000, chunk_overlap=100)
        doc_split = text_splitter.split_documents(doc_list)

        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorestore = FAISS.from_documents(doc_split,embeddings)
        rag_retriever = vectorestore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

        #st.session_state.rag_retriever = vectorestore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

        #rag_retriever = st.session_state.rag_retriever

        #rag_retriever = st.session_state.rag_retriever
        return rag_retriever
