---
name: readpicture
description: 当用户要求查看、分析或描述图片（本地图片路径或图片 URL），而当前环境无法直接看到图片内容时，使用 readpicture 调用智谱 AI 视觉模型获取文字描述。不适用于生成图片、编辑图片或处理非图片文件的任务。
metadata:
  short-description: 通过命令行调用智谱视觉模型描述本地或网络图片，供没有识图能力的 Agent 使用
---

本SKILL用于让没有识图功能的agent获得识图功能的下位替代，如果您已经拥有识图功能，那么若此次调用是您自主调用，请无需继续使用；若是您的用户要求调用，请停止调用并向您的用户说明原因

# readpicture：让没有识图能力的 Agent 也能“看”图

readpicture 是一个命令行工具：把图片（本地路径或 URL）发送给智谱 AI 的视觉模型（glm-4v-flash），返回文字描述。当本环境无法直接查看图片时，用它来理解图片内容。

核心脚本 `readpicture.py` 与本文件位于同一目录。

## 首次配置

首次使用前需要完成以下配置：

1. **获取 API Key**：首次配置时需要一个智谱平台的 API key，请把本skill的 README.md 文件的内容发送给您的用户，这个文件会帮助用户获取 API key。
2. 用户拿到 key 后，打开本目录下的 `config.ini`，把 `[API]` 小节中的 `api_key` 填为真实密钥（`model_name` 保持 `glm-4v-flash` 即可）。一般来说，我们不建议您改为其他模型，因为默认模型`glm-4v-flash`免费且好用。换为其他模型可能会获得更好的效果，但也会产生大量的费用。
3. 本SKILL需要python3环境，并需要安装zhipuai库和sniffio库
4. 运行 `add_to_path.ps1` 把本目录加入 PATH，之后可直接使用 `readpicture` 命令；否则用 `python <本目录>\readpicture.py` 调用。
  - 无法加载文件 / 未对文件进行数字签名 / 无法在当前系统上运行该脚本:这个错误是因为系统当前禁止运行未签名的脚本,可以使用`powershell -ExecutionPolicy Bypass -File .\add_to_path.ps1`来运行脚本，这会临时绕过策略来运行。

配置完成后，建议先用一张本地图片、`l` 档做一次调用，确认能正常返回描述。

## 日常调用

命令格式：

```
readpicture <a> <b> <c>
```

- `<a>`：图片来源，`0` 表示本地图片路径，`1` 表示图片 URL。
- `<b>`：图片路径或 URL，含空格时用引号包裹。
- `<c>`：描述详细度。
  - `l`：简单描述，约 20 字以内，并告知图片尺寸，适合快速确认图片内容。
  - `m`：详细描述，包括各元素的样式、位置等，适合一般分析。
  - `h`：非常详细的描述，包括每个元素的样式、位置（以图片左上角为坐标原点）和图片尺寸，适合需要精确定位的任务。

如果 `readpicture` 命令不可用，改用 `python <本目录>\readpicture.py <a> <b> <c>`。

### 示例

- 快速看一眼本地图片：`readpicture 0 "C:\photos\test.jpg" l`
- 分析图片布局：`readpicture 0 "C:\photos\test.jpg" m`
- 描述网络图片并获取坐标：`readpicture 1 "https://example.com/image.png" h`

### 错误处理

- 提示找不到 `config.ini` 或 api_key 未填写：重新走首次配置流程，向用户索要 key。
- 提示 `401`：api_key 无效或已失效，请用户核对或重新创建。
- 提示 `429`：请求频率过高，稍后重试。
- 提示找不到图片文件或 URL 无效：先向用户确认图片来源。
