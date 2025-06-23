import os
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()
print("=== 调试信息 ===")
print(f"当前工作目录: {os.getcwd()}")
print(f"DEEPSEEK_API_KEY 环境变量: {os.getenv('DEEPSEEK_API_KEY')}")
print(f".env 文件是否存在: {os.path.exists('.env')}")

# 创建 AI 蓝图
ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

# 初始化 DeepSeek 客户端
try:
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
    )
except Exception as e:
    print(f"AI客户端初始化失败: {e}")
    client = None


@ai_bp.route("/chat", methods=["POST"])
def ai_chat():
    """AI 聊天接口"""
    if not client:
        return jsonify({"error": "AI服务未正确配置", "status": "error"}), 500

    try:
        data = request.get_json()
        user_question = data.get("question", "")

        if not user_question.strip():
            return jsonify({"error": "问题不能为空", "status": "error"}), 400

        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个水质监测和海洋环境专家，专门回答关于水质、环境监测、海洋生态相关的问题。请用简洁专业的语言回答。",
                },
                {"role": "user", "content": user_question},
            ],
            stream=False,
            max_tokens=500,
            temperature=0.7,
        )

        ai_answer = response.choices[0].message.content

        return jsonify({"answer": ai_answer, "status": "success"})

    except Exception as e:
        print(f"AI API调用错误: {str(e)}")
        return (
            jsonify({"error": "AI服务暂时不可用，请稍后再试", "status": "error"}),
            500,
        )


@ai_bp.route("/health", methods=["GET"])
def ai_health():
    """AI 服务健康检查"""
    if not client:
        return jsonify({"status": "unhealthy", "message": "AI客户端未初始化"}), 500

    return jsonify({"status": "healthy", "message": "AI服务正常"})
