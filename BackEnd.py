from flask import Flask, request, jsonify, render_template
from gherkin.parser import Parser
from gherkin.errors import CompositeParserException

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('frontEnd.html')

@app.route('/check_parsing_error', methods=['POST'])
def check_parsing_error():
    file = request.files['file']
    feature_content = file.read().decode('utf-8')

    parser = Parser()
    errors = []

    try:
        parser.parse(feature_content)
    except CompositeParserException as e:
        for error in e.errors:
            line = error.location['line']
            if line - 1 < len(feature_content.splitlines()):
                errors.append((line, feature_content.splitlines()[line - 1].strip()))  # Trim spaces

    errors = [f"{i + 1}. {error[1]} :: Error found in Line number = {error[0]}" for i, error in enumerate(errors)]  # Add numbering and line number
    if not errors:
        errors.append('No parsing error, great job!')
    return jsonify(errors=errors, total=len(errors))

if __name__ == '__main__':
    app.run(debug=True)
