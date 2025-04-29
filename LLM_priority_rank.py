from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def llm_rank(input_message, input_identity):

    llm = ChatOpenAI(
        model_name="gpt-4o-mini"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a concise assistant that helps summarize and prioritize emails based on their urgency and relevance. The user receiving this email is identified as: {user_identity}. Evaluate the urgency and importance of the email in relation to this user's role. Assign a priority score from 1 to 5, where:\n"
         "- 1 = Low priority (general information, newsletters, non-urgent)\n"
         "- 2 = Mildly relevant (optional events, minor requests)\n"
         "- 3 = Moderate importance (work-related updates, project discussions)\n"
         "- 4 = High importance (urgent requests, meeting schedules)\n"
         "- 5 = Critical (time-sensitive issues, legal/financial matters)\n"
         "Present the output in the following format: 'Priority: [1-5]'."),
        ("user", "Email Content:\n{email_content}")
    ])

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    output = chain.invoke({"email_content": input_message, "user_identity": input_identity})

    return output

