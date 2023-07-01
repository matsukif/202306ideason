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
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    st.session_state["messages"].append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"]
    )  

    bot_message = {"role": "assistant", "content": response["choices"][0]["message"]["content"]}
    st.session_state["messages"].append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("レストランの口コミを要約します")
st.write("レストランの口コミを入力してください")
st.write("概要、雰囲気、人気メニュー、接客態度、ペット店内可否の５つの観点で整理します")

# ユーザーからの口コミ入力
review_input = st.text_area("レストランの口コミ", key="review_input")

# ユーザーからの観点指定入力
aspect_input = st.text_input("要約の観点を指定してください（例：概要、雰囲気、人気メニュー、接客態度、ペット店内可否）", key="aspect_input")

# 口コミと観点を結合して全体のユーザー入力を作成
st.session_state["user_input"] = f"{review_input}\n{aspect_input}"

if st.button("Submit"):
    communicate()

if st.session_state["messages"]:
    for message in reversed(st.session_state["messages"]):  # 直近のメッセージを上に
        speaker = "＜口コミ情報＞"
        if message["role"]=="assistant":
            speaker="＜要約結果＞"

        st.write(speaker)
        st.write(message["content"])
