from flask import Flask, jsonify

app = Flask(__name__)


# This is our custom middleware to enable Design by Contract.
# We need to make sure that we use assert statements throughout the
# business logic to be able to give back proper exceptions
@app.errorhandler(500)
def handle_internal_server_error(error):
    response = jsonify({"message": "Internal Server Error", "error": str(error)})
    response.status_code = 500
    return response


@app.route("/example")
def example_route():
    try:
        # Your code here
        assert False, "This is an example AssertionError"
        return jsonify({"message": "Success"})
    except AssertionError as e:
        raise e

# This is an application that exposes routes for a calculator.
# It has a route for addition, subtraction, multiplication and division.
# Each route expects two query parameters, a and b, which are the numbers
# Each route is implemented in a framework-agnostic method and a seperate flask method that handles the request
# Integrity is ensured via asserts so the application can handle the errors gracefully

if __name__ == "__main__":
    app.run()
