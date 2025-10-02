import os
text = "Gib mir ein kurzes motivierendes Zitat."
if os.getenv("OPENAI_API_KEY"):
    from langchain_openai import ChatOpenAI
    from langchain.schema import HumanMessage
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    res = llm([HumanMessage(content=text)])
    print("LangChain:", res.content)
else:
    print("LangChain Fallback:", f"Echo: {text}")
