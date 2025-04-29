


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 好怪哦，我都没有输入 Openai key 它就自动运行模型了，感觉是这个电脑记住了我的 openai key，当部署到服务器的时候就不能这样了

def llm_summary(input_message):

    llm = ChatOpenAI(
        model_name="gpt-4o-mini"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise assistant. Summarize the email body into a single, short sentence (20-25 words max) that answers what, when, and where. If the email body contains at least one Japanese sentence, the output must be in Japanese; otherwise, it should be in English. Highlight key terms using ** for quick comprehension, but avoid marking the same keyword multiple times. Ensure the summary remains clear and concise, avoiding unnecessary phrases or redundant information."),
        ("user", "{input}")
    ])

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    output = chain.invoke({"input": input_message})

    return output


