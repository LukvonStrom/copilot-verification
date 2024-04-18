from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    # Get the user input from the request
    user_input = request.json.get('data', '')

    # Precondition: Check that the input is not too long
    assert len(user_input) <= 100, "Input too long!"

    # Precondition: Check that the input can be converted to an integer
    try:
        numeric_input = int(user_input)
    except ValueError:
        return "Invalid input! Must be an integer.", 400

    # Process the numeric input
    result = 0
    if numeric_input < 0:
        result = "Negative value received!"
    else:
        result = numeric_input + 1

    # Postcondition: Ensure that the result is either a string (for negative input message) or an integer incremented by 1
    assert isinstance(result, int) or (isinstance(result, str) and result == "Negative value received!"), "Invalid result type!"

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
