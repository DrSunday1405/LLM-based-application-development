
# 主函数代码

from messages_from_gmail_api import list_gmail_api_messages
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



def llm_user_id(mail_id):

    query = ""   # 邮件筛选标准
    count = 20  # 最大返回邮件数

    messages = list_gmail_api_messages(mail_id, query, count)


    Email_sample_list = messages[0:20]

    llm = ChatOpenAI(
            model_name="gpt-4o-mini"
        )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an intelligent assistant tasked with analyzing a user's email history to infer their likely professional role. Given the content of recent emails, including senders, subjects, and key phrases, determine the most probable identity of the user. Output only the inferred role in one concise sentence, ensuring it includes the user's profession, specific field of expertise, and institution or company (if applicable). Avoid additional explanations, reasoning, or analysis."),
        ("user", "{input}")
    ])

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    output = chain.invoke({"input": Email_sample_list})

    print("The user identity is:")
    print(output)

    return output




