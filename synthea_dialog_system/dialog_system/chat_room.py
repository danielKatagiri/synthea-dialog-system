import pandas as pd
import streamlit as st

from .llm_engine import create_llm_engine
from .query_engine import create_query_engine, prompt_template
from .text_helpers import preprocess_possible_json


def start_chat_room():
    st.title("Synthea Dialog System")

    query_engine = create_query_engine()
    llm_chain = create_llm_engine()

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What information do you want to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            response = llm_chain.run(input=prompt)
            st.markdown(prompt)

        llm_response = preprocess_possible_json(response)
        print(llm_response)

        if llm_response["sql"]:
            formatted_prompt = prompt_template.format(input=llm_response["question"])
            sql_response = query_engine.query(formatted_prompt)
            response = sql_response.response
        else:
            response = llm_response["answer"]

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = response
            message_placeholder.markdown(full_response)

            if llm_response["figure"]:
                print(sql_response.metadata["sql_query"])

                df = pd.DataFrame(
                    {"gender": ["male", "female"], "average_age": [54, 56]}
                )
                st.bar_chart(df, x="gender", y="average_age")

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
