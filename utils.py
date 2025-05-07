from some_vector_store_library import Retriever  # ベクターストア用ライブラリをインポート
from some_llm_library import LLM  # LLM用ライブラリをインポート

# ベクターストアのRetrieverを初期化
retriever = Retriever()  # 適切な初期化を行ってください

# LLMを初期化
llm = LLM()  # 適切な初期化を行ってください

def build_prompt(chat_message, related_docs):
    """
    ユーザーの入力と関連ドキュメントを基にプロンプトを生成する関数。
    """
    prompt = f"ユーザーの質問: {chat_message}\n\n関連ドキュメント:\n"
    for i, doc in enumerate(related_docs, start=1):
        prompt += f"{i}. {doc['content']}\n"
    prompt += "\n回答:"
    return prompt

def get_llm_response(chat_message):
    """
    ベクターストアから関連ドキュメントを取得し、LLMにプロンプトを渡して回答を生成する関数。
    """
    try:
        # ベクターストアから関連ドキュメントを取得（5件）
        related_docs = retriever.get_relevant_documents(chat_message, top_k=5)

        # プロンプトを生成
        prompt = build_prompt(chat_message, related_docs)

        # LLMにプロンプトを渡して回答を生成
        response = llm.generate_response(prompt)

        return response

    except Exception as e:
        # エラーが発生した場合は例外をスロー
        raise RuntimeError(f"LLM応答生成中にエラーが発生しました: {e}")