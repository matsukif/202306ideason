import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドでは以下ルールを厳格に守ってください。
あなたはレストランの評判情報から以下の５点を整理して回答するシステムです。
・レストランの概要
・レストランの雰囲気
・人気メニュー
・接客態度
・ペット店内可否

レストランの評判情報は複数の人が記載したものを「改行」でつないで入力します。

"""


# st.session_stateを使いメッセージのやりとりを保存
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [
#         {"role": "system", "content": system_prompt}
#         ]

# チャットボットとやりとりする関数
def communicate():
#    messages = st.session_state["messages"]
    messages = {"role": "system", "content": system_prompt}
   
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("レストランの口コミを要約します。")
#st.image("bom_v2.1.png")
st.write("レストランの口コミを入力してください")
# st.write("例：Toyosu Building, 3-3-3 Toyosu, Koto-ku, Tokyo, Japan")

user_input = st.text_input("レストランの口コミ", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
