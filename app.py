
import streamlit as st
from openai import OpenAI

# Streamlit Community Cloud の Secrets から OpenAI API Key を取得する
client = OpenAI(
  api_key = st.secrets.OpenAIAPI.openai_api_key,
)

# メッセージのやり取りを保存する
if "messages" not in st.session_state:
  st.session_state["messages"] = [
    {
      "role": "system",
      "content": st.secrets.AppSettings.chatbot_setting
    }
  ]

# チャットボットとやり取りする関数
def communicate():
  messages = st.session_state["messages"]

  user_message = {
    "role": "user",
    "content": st.session_state["user_input"]
  }
  messages.append(user_message)

  response = client.chat.completions.create(
    # model="gpt-3.5-turbo",
    model="gpt-4",
    messages=messages,
    temperature=1.0 # ★★★
  )

  # bot_message = response["choices"][0]["message"]
  bot_message = response.choices[0].message
  messages.append(bot_message)

  st.session_state["user_input"] = "" #入力欄を消去

# UI
st.title("勉強をサポートするねこ")
st.image("logo.png")
# st.write("勉強で分からないことについて答えたり練習問題を出すことができます。")

user_input = st.text_input(
  "勉強で分からないことについて答えたり練習問題を出すことができます。",
  key="user_input",
  on_change=communicate
)

if st.session_state["messages"]:
  messages = st.session_state["messages"]

  for message in reversed(messages[1:]): # 直近のメッセージを上に
    speaker = "🙂" # 相談者
    # if message["role"]=="assistant":
    if message.role=="assistant":
      speaker="😺" # チャットボット

    st.write(speaker + ": " + message["content"])
