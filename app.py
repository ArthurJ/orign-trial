import json
from risk_engine import process, eligibility, general_rules, risk_specific_rules, risk_modifiers 
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/risk_profile', methods=['POST'])
def index():
    print(request.json)
    return jsonify( 
            process(request.json, 
                    general_rules, 
                    eligibility, 
                    risk_specific_rules,
                    risk_modifiers))


if __name__ == '__main__':
    app.run(debug=True)