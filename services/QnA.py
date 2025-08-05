from schemas.QnA import ChatbotRequest
from langchain_community.utilities import SQLDatabase
from database import db
from services.embedding_tool import noun_handling_tool
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory


# to load gemini api
load_dotenv()

# llm initialization
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0,
    convert_system_message_to_human=True,
    max_tokens=2000,
    max_retries=2,
)

# sql toolkit initialization
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

system_message = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.

""".format(
    dialect="SQL Server",
    top_k=5,
)

# memory handling
store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# uncomment following tool to handle user`s spelling mistakes and not exact machings. but its too resource consuming`

# retriever_tool = noun_handling_tool(db)

# suffix = (
#     "If you need to filter on a proper noun like a Name, you must ALWAYS first look up "
#     "the filter value using the 'search_proper_nouns' tool! Do not try to "
#     "guess at the proper name - use this function to find similar ones."
# )

# system_message = f"{system_message}\n\n{suffix}"

# tools.append(retriever_tool)


#  agent initialization
try:
    agent = create_react_agent(llm, tools, system_message)
    agent_with_memory = RunnableWithMessageHistory(
        agent,
        get_session_history,
        input_messages_key="messages",
    )
except ImportError as e:
    print(f"error while initializing agent :{e}")


#  endpoint function
async def get_chatbot_response(query: ChatbotRequest):

    user_question = query.query.strip()

    try:
        response = await agent_with_memory.ainvoke(
            {"messages": [{"role": "user", "content": user_question}]},
            config={
                "configurable": {"session_id": "test_id"}
            },  # session id need to handle
        )

        if isinstance(response, dict) and "messages" in response:
            messages = response["messages"]

            # The last message in the list is the final response
            if messages and len(messages) > 0:
                last_message = messages[-1]

                # The final message's content is the answer
                if hasattr(last_message, "content"):
                    return last_message.content
                elif isinstance(last_message, dict) and "content" in last_message:
                    return last_message["content"]

            return "No response generated from agent."

        # Fallback for unexpected formats
        return str(response)

    except Exception as e:
        error_msg = str(e)
        print(f" agent invoking error: {error_msg}")
        return f"error occurred while processing: {error_msg}"
