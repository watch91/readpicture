import sys
import base64
import os
import configparser
from zhipuai import ZhipuAI

# ------------------- 读取配置 -------------------
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        print(f"错误：找不到配置文件 '{CONFIG_FILE}'，请确保它与本脚本在同一目录下。")
        print("请参考以下格式创建 config.ini：")
        print("[API]")
        print("api_key = 你的API密钥")
        print("model_name = glm-4v-flash")
        sys.exit(1)

    config.read(CONFIG_FILE, encoding='utf-8')
    try:
        api_key = config.get('API', 'api_key')
        model_name = config.get('API', 'model_name', fallback='glm-4v-flash')
    except configparser.NoSectionError:
        print("错误：配置文件缺少 [API] 节，请检查 config.ini 格式。")
        sys.exit(1)
    except configparser.NoOptionError as e:
        print(f"错误：配置文件缺少选项 {e}，请检查。")
        sys.exit(1)

    if not api_key or api_key == "你的API密钥":
        print("错误：请在 config.ini 中填写正确的 api_key。")
        sys.exit(1)

    return api_key, model_name

API_KEY, MODEL_NAME = load_config()
# -----------------------------------------------

def encode_image(image_path):
    """读取本地图片，返回 base64 编码的 Data URI"""
    try:
        with open(image_path, "rb") as f:
            img_data = f.read()
        b64 = base64.b64encode(img_data).decode('utf-8')
        # 根据扩展名粗略判断 MIME 类型
        ext = os.path.splitext(image_path)[1].lower()
        mime = "image/jpeg"
        if ext in ['.png']:
            mime = "image/png"
        elif ext in ['.webp']:
            mime = "image/webp"
        elif ext in ['.gif']:
            mime = "image/gif"
        return f"data:{mime};base64,{b64}"
    except FileNotFoundError:
        print(f"错误：找不到文件 '{image_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"读取图片失败: {e}")
        sys.exit(1)

def get_prompt(level):
    """根据详细程度返回提示词"""
    prompts = {
        'l': "请简单描述图片，不超过80字，并告知图片尺寸",
        'm': "请详细描述图片，包括图片中每一个元素的样式、位置等，并告知图片尺寸",
        'h': "请十分详细的描述图片，包括图片中每一个元素的样式、位置（以图片左上角为坐标原点，输出详细坐标）等，并告知图片尺寸"
    }
    return prompts.get(level, prompts['m'])

def describe_image(image_source, source_type, prompt):
    """调用模型获取描述"""
    client = ZhipuAI(api_key=API_KEY)

    if source_type == 0:
        img_uri = encode_image(image_source)
    else:
        img_uri = image_source

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": img_uri}}
            ]
        }
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"API 调用失败: {e}")
        if "401" in str(e):
            print("提示：请检查 config.ini 中的 api_key 是否正确。")
        elif "429" in str(e):
            print("提示：请求频率过高，请稍后再试。")
        sys.exit(1)

def print_usage():
    print("用法: readpicture <a> <b> <c>")
    print("  <a> : 0 (本地图片路径) 或 1 (图片 URL)")
    print("  <b> : 图片路径或 URL")
    print("  <c> : l (低详细度) | m (中详细度) | h (高详细度)")
    print("示例:")
    print("  readpicture 0 \"C:\\photos\\test.jpg\" m")
    print("  readpicture 1 \"https://example.com/image.png\" h")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)

    a = sys.argv[1]
    b = sys.argv[2]
    c = sys.argv[3].lower()

    if a not in ('0', '1'):
        print("错误：<a> 必须为 0 或 1")
        print_usage()
        sys.exit(1)
    if c not in ('l', 'm', 'h'):
        print("错误：<c> 必须为 l、m 或 h")
        print_usage()
        sys.exit(1)

    source_type = int(a)
    image_source = b
    prompt = get_prompt(c)

    describe_image(image_source, source_type, prompt)