from flask import Flask, render_template, request, jsonify
import time
from agents.creative_agent import CreativeAgent
from agents.editor_agent import EditorAgent
from agents.coder_agent import CoderAgent
from agents.critic_agent import CriticAgent

app = Flask(__name__)

creative_agent = CreativeAgent()
editor_agent = EditorAgent()
coder_agent = CoderAgent()
critic_agent = CriticAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_content():
    data = request.json
    theme = data.get('theme', '未来科技')
    content_type = data.get('type', 'poem')

    result = {'steps': []}

    step1 = creative_agent.generate(theme, content_type)
    step2 = editor_agent.refine(step1, content_type)
    final_content = step2

    score, feedback = critic_agent.evaluate(final_content, content_type)

    result.update({
        "final_result": final_content,
        "score": score,
        "feedback": feedback,
        "steps": [
            {"agent": "创意Agent", "content": step1},
            {"agent": "优化Agent", "content": step2},
        ]
    })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
