# 使用 Gmail api 读取邮件


# 尝试读取邮件
import base64
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from apiclient import errors
import logging
from gmail_credential import get_credential

logger = logging.getLogger(__name__)

def decode_base64url_data(data):
    """
    base64url のデコード
    """
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_message = decoded_bytes.decode("UTF-8")
    return decoded_message


def list_gmail_api_messages(user_id, query, count):

    creds = get_credential()   # 新用户会通过这一步进行授权，然后我们的应用就这样获得 access token
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    messages = []
    try:
        message_ids = (
            service.users()
            .messages()
            .list(userId=user_id, maxResults=count, q=query, labelIds=["INBOX"])
            .execute()
        )
       # 如果你现在访问的邮箱没有 access token，这一步就会报错
        # 注意：这里用的是 list() 函数，只是获取邮件的 id，并没有获取邮件的详细内容
        # 要想获取邮件详细内容，还得是下面的 get()函数


        # message_ids is a dictionary ？
        if message_ids["resultSizeEstimate"] == 0:
            logger.warning("no result data!")
            return []

        # message id を元に、message の内容を確認
        for message_id in message_ids["messages"]:
            message_detail = (
                service.users()
                .messages()
                .get(userId = user_id, id = message_id["id"])
                .execute()
            )

            message = {}
            # 其实message 就是 message_detail 的一个副本，只不过我们是先将 message_detail 里面的内容先解码，再赋值给message
            message["id"] = message_id["id"]
            # 単純なテキストメールの場合
            if 'data' in message_detail['payload']['body']:  # 其实 message_detail 里面就是字典的多层嵌套
                message["body"] = decode_base64url_data(
                    message_detail["payload"]["body"]["data"]
                )
            # html メールの場合、plain/text のパートを使う

            else:
                parts = message_detail['payload']['parts']
                # print("debug")
                # print(parts)
                # print("\n")
                content_part = [part for part in parts if part['mimeType'] == 'text/plain'] # 它把选出来的字典类型变成列表的形式
                if content_part:
                    message["body"] = decode_base64url_data(
                    content_part[0]['body']['data']    # content_part其实就是一个只有一个元素的列表，这个元素就是选出来的字典
                    )
                else:
                    content_part = [part for part in parts if part['mimeType'] == 'multipart/alternative']
                    message["body"] = decode_base64url_data(
                        content_part[0]['parts'][0]['body']['data']  # content_part其实就是一个只有一个元素的列表，这个元素就是选出来的字典
                    )
            # print(message["body"])
            # print("\n")
            # else:
            #     parts = message_detail['payload']['parts']
            #     plain_parts = [part for part in parts if part['mimeType'] == 'text/plain']
            #
            #     if plain_parts:
            #         message["body"] = decode_base64url_data(plain_parts[0]['body']['data'])
            #
            #     # 如果没有 text/plain，尝试提取 text/html 部分
            #     else:
            #         html_parts = [part for part in parts if part['mimeType'] == 'text/html']
            #         if html_parts:
            #             html_content = decode_base64url_data(html_parts[0]['body']['data'])
            #             soup = BeautifulSoup(html_content, 'html.parser')
            #             message["body"] = soup.get_text()
            #         else:
            #             message["body"] = "No text/plain or text/html content found."

            # payload.headers[name: "Subject"]
            message["subject"] = [
                header["value"]
                for header in message_detail["payload"]["headers"]
                if header["name"] == "Subject"
            ][0]
            # payload.headers[name: "From"]
            message["from"] = [
                header["value"]
                for header in message_detail["payload"]["headers"]
                if header["name"] == "From"
            ][0]
            logger.info(message_detail["snippet"])
            messages.append(message)
        return messages

    except errors.HttpError as error:
        print("An error occurred: %s" % error)




