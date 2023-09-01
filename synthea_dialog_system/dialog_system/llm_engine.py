from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory.buffer import ConversationBufferMemory


def create_llm_engine():
    template = """
        Current conversation:
        {history}

        I am a data analyst and a have a database running with information about patients and conditions.
        Analyse the following question and answer if the question can be answered by running a SQL query.
        The result should be in a JSON format, as follows:
        ```json
        {{
            "sql": bool, # This field should be true if the question can be answered with data on patients and conditions, else should be false
            "figure": bool, # This field should be true if the answer can be shown with a 2 dimensional figure
            "question": str, # Rewrite the question, using natural language, making the question more clearer.
            "answer": str, # This field is the answer you would give to the question asked. If the AI does not know the answer to a question, it truthfully says it does not know in this field.
        }}
        ```
        No explanation is needed. Return only the json.
        Answer the question: {input}
    """

    prompt = PromptTemplate(input_variables=["history", "input"], template=template)

    chain = ConversationChain(
        prompt=prompt,
        llm=ChatOpenAI(model="gpt-4"),
        verbose=False,
        memory=ConversationBufferMemory(),
    )

    return chain
