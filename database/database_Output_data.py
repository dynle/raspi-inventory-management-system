import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time
import sqlite3

load_dotenv()

def fetch_channel_messages(client, channel_id, limit=10):
    try:
        response = client.conversations_history(channel=channel_id, limit=limit)
        messages = response['messages']
        return messages[0]
    except SlackApiError as e:
        print(f"Error fetching conversations: {e.response['error']}")
        return None
    
def send_message(client, channel_id, text):
    try:
        response = client.chat_postMessage(channel=channel_id, text=text)
        print(f"Message sent: {response['ts']}")
    except SlackApiError as e:
        print(f"error sending message: {e.response['error']}")


def main():
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
    CHANNEL_ID = os.getenv('CHANNEL_ID')

    client = WebClient(token=SLACK_BOT_TOKEN)

    last_message_ts = None
    is_send = False
    
    bot_user_id = client.auth_test()["user_id"]
    
    while True:
        latest_message = fetch_channel_messages(client, CHANNEL_ID)
        if latest_message:
            latest_message_ts = latest_message.get('ts')
            if latest_message_ts != last_message_ts:
                last_message_ts = latest_message_ts
                user_id = latest_message.get('user')
                print(latest_message.get('text'))
                mess= latest_message.get('text')
                if len(mess.split()) == 3:
                    mode,year,month = mess.split()
                else:
                    print("error: message must be consists of 3 parts.")
                    continue
                year=int(year)
                month=int(month)
                if mode == 'sum' and user_id != bot_user_id:
                    #send message by bot
                    conn = sqlite3.connect('IIC_base.db')
                    cursor = conn.cursor()
                    query='''
                    SELECT *
                    FROM user
                    '''
                    cursor.execute(query)
                    results = cursor.fetchall()
                    print(results)
                    query='''
                    SELECT *
                    FROM product
                    '''
                    cursor.execute(query)
                    results = cursor.fetchall()
                    print(results)
                    query = '''
                    SELECT user_Name, SUM(price) as total_amount
                    FROM user
                    JOIN product ON user.item_name = product.item_name
                    WHERE Year = ? AND Month = ?
                    GROUP BY user_Name
                    ORDER BY total_amount DESC;
                    '''
                    cursor.execute(query, (year, month))
                    
                    results = cursor.fetchall()
                    response = ""
                    for row in results:
                        print(results)
                        response += f"ユーザー: {row[0]}, {year}年{month}月, 合計金額: {row[1]}円\n"
                
                    #send_message(client, CHANNEL_ID, f"{response}")
                    print(f"response: {response}")
                    send_message(client, CHANNEL_ID, response)
                    conn.commit()
                    conn.close()
          
        time.sleep(1)  
        
if __name__ == "__main__":
    main()