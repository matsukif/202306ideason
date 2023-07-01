import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドでは以下ルールを厳格に守ってください。
あなたはレストランの評判情報から以下を整理して回答するシステムです。
・レストランの概要
・レストランの雰囲気
・人気メニュー
・接客態度
"""


# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
# def communicate():
#     user_message = {"role": "user", "content": st.session_state["user_input"]}
#     st.session_state["messages"].append(user_message)

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=st.session_state["messages"]
#     )  

#     bot_message = response["choices"][0]["message"]
#     messages.append(bot_message)

#     st.session_state["user_input"] = ""  # 入力欄を消去

#chatGPTが修正したコード
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
st.write("概要、雰囲気、人気メニュー、接客態度の４つの観点で整理します。")
st.write("また観点を１つ追加することもできます。")

# ユーザーからの観点指定入力
aspect_input = st.text_input("追加したい観点（例：ペット可否）", key="aspect_input")

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
    
# ユーザーからの口コミ入力
review_input = st.text_area("レストランの口コミ", key="review_input")
    
if st.button("要約開始"):
    # 追加観点のプロンプトに追加
    # if aspect_input != "":
    #     system_prompt_added = "\n・".join([system_prompt, aspect_input])
    #     st.session_state["messages"] = [
    #         {"role": "system", "content": system_prompt_added}
    #         ]
    
    st.session_state["user_input"] = review_input  # 追加する行
    #st.session_state["user_input"] = st.text_area("レストランの口コミ", key="user_input")  # ここに移動
    
    communicate()

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "＜口コミ情報＞"
        if message["role"]=="assistant":
            speaker="＜要約結果＞"

        # st.write(speaker + ": " + message["content"])
        st.write(speaker)
        st.write(message["content"])
