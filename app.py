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

# ユーザーからの各観点の入力
overview = st.text_input("レストランの概要", key="overview")
atmosphere = st.text_input("レストランの雰囲気", key="atmosphere")
popular_menu = st.text_input("人気メニュー", key="popular_menu")
customer_service = st.text_input("接客態度", key="customer_service")
pet_friendly = st.text_input("ペット店内可否", key="pet_friendly")

# 観点を結合して全体のユーザー入力を作成
st.session_state["user_input"] = f"{overview}\n{atmosphere}\n{popular_menu}\n{customer_service}\n{pet_friendly}"
communicate()

if st.session_state["messages"]:
    messages = st.session_state
