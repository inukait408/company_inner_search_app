from dotenv import load_dotenv
import logging
import streamlit as st
import utils
from initialize import initialize
import components as cn
import constants as ct

st.set_page_config(
    page_title=ct.APP_NAME
)

# ログ出力を行うためのロガーの設定
logger = logging.getLogger(ct.LOGGER_NAME)

def handle_error(logger, error_message, exception):
    """
    エラーハンドリングを共通化する関数。
    """
    logger.error(f"{error_message}\n{exception}")
    st.error(utils.build_error_message(error_message), icon=ct.ERROR_ICON)
    st.stop()

def initialize_session_state():
    """
    セッション状態を初期化する関数。
    """
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = []

# セッション状態の初期化
initialize_session_state()

try:
    # 初期化処理（「initialize.py」の「initialize」関数を実行）
    initialize()
except Exception as e:
    handle_error(logger, ct.INITIALIZE_ERROR_MESSAGE, e)

# アプリ起動時のログファイルへの出力
logger.info(ct.APP_BOOT_MESSAGE)

# タイトル表示
cn.display_app_title()

# モード表示
cn.display_select_mode()

# AIメッセージの初期表示
cn.display_initial_ai_message()

try:
    # 会話ログの表示
    cn.display_conversation_log()
except Exception as e:
    handle_error(logger, ct.CONVERSATION_LOG_ERROR_MESSAGE, e)

# ユーザー入力を受け取る
chat_message = st.chat_input(ct.CHAT_INPUT_HELPER_TEXT)

if chat_message:
    # ユーザーメッセージのログ出力
    logger.info({"message": chat_message, "application_mode": st.session_state.mode})

    # ユーザーメッセージを表示
    with st.chat_message("user"):
        st.markdown(chat_message)

    # 「st.spinner」でグルグル回っている間、表示の不具合が発生しないよう空のエリアを表示
    res_box = st.empty()

    # LLMによる回答生成（回答生成が完了するまでグルグル回す）
    with st.spinner(ct.SPINNER_TEXT):
        try:
            # 画面読み込み時に作成したRetrieverを使い、Chainを実行
            llm_response = utils.get_llm_response(chat_message)
        except Exception as e:
            handle_error(logger, ct.GET_LLM_RESPONSE_ERROR_MESSAGE, e)

    # AIの応答を表示
    with st.chat_message("assistant"):
        try:
            # モードが「社内文書検索」の場合
            if st.session_state.mode == ct.ANSWER_MODE_1:
                content = cn.display_search_llm_response(llm_response)

            # モードが「社内問い合わせ」の場合
            elif st.session_state.mode == ct.ANSWER_MODE_2:
                content = cn.display_contact_llm_response(llm_response)

            # AIメッセージのログ出力
            logger.info({"message": content, "application_mode": st.session_state.mode})

        except Exception as e:
            handle_error(logger, ct.DISP_ANSWER_ERROR_MESSAGE, e)

    # 表示用の会話ログにユーザーメッセージを追加
    st.session_state.messages.append({"role": "user", "content": chat_message})

    # 表示用の会話ログにAIメッセージを追加
    st.session_state.messages.append({"role": "assistant", "content": content})
