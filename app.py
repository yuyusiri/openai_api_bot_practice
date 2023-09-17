
import streamlit as st
import openai

# Streamlit Community Cloud の Secrets から OpenAI API Key を取得する
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

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

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=1.0 # ★★★
  )

  bot_message = response["choices"][0]["message"]
  messages.append(bot_message)

  st.session_state["user_input"] = "" #入力欄を消去

# UI
st.title("勉強をサポートするねこ")
st.image("logo.png")
# st.write("勉強について知りたいことは何ですか？")

user_input = st.text_input(
  "勉強について知りたいことを入力してください",
  key="user_input",
  on_change=communicate
)

if st.session_state["messages"]:
  messages = st.session_state["messages"]

  for message in reversed(messages[1:]): # 直近のメッセージを上に
    speaker = "🙂" # 相談者
    if message["role"]=="assistant":
      speaker="😺" # チャットボット

    st.write(speaker + ": " + message["content"])
