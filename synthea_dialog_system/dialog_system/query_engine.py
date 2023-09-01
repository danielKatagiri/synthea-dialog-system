import streamlit as st
from langchain.chat_models import ChatOpenAI
from llama_index import LLMPredictor, ServiceContext, SQLDatabase, VectorStoreIndex
from llama_index.indices.struct_store import SQLTableRetrieverQueryEngine
from llama_index.objects import ObjectIndex, SQLTableNodeMapping, SQLTableSchema
from llama_index.prompts import PromptTemplate
from sqlalchemy import MetaData

from ..database import ENGINE


@st.cache_resource(show_spinner=True)
def create_query_engine():
    metadata_obj = MetaData()
    metadata_obj.reflect(ENGINE)

    sql_database = SQLDatabase(ENGINE)
    table_node_mapping = SQLTableNodeMapping(sql_database)

    table_schema_objs = []
    for table_name in metadata_obj.tables.keys():
        table_schema_objs.append(SQLTableSchema(table_name=table_name))

    obj_index = ObjectIndex.from_objects(
        table_schema_objs,
        table_node_mapping,
        VectorStoreIndex,
    )

    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    )
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    query_engine = SQLTableRetrieverQueryEngine(
        sql_database,
        obj_index.as_retriever(similarity_top_k=1),
        service_context=service_context,
    )

    return query_engine


prompt_template = PromptTemplate(
    """
{input}
Keep in mind that to compute the patient's age, you have to use the birth_date columns.
"""
)
