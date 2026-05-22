from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/execute', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    
    if not code.strip():
        return jsonify({"output": "يرجى كتابة كود بُرهان للبدء...", "error": False})


    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        output = interpreter.run(ast)
        
        return jsonify({"output": str(output), "error": False})
        
    except Exception as e:
        return jsonify({"output": f" خطأ: {str(e)}", "error": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)


   
 #app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))