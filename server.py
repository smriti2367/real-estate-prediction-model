from flask import Flask, request, jsonify
from artifacts import abc_1

app = Flask(__name__)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': abc_1.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        # Check if the request is JSON
        if request.is_json:
            data = request.get_json()
            total_sqft = float(data['total_sqft'])
            location = data['location']
            bhk = int(data['bhk'])
            bath = int(data['bath'])
        else:
            # If not JSON, assume it's form data
            total_sqft = float(request.form['total_sqft'])
            location = request.form['location']
            bhk = int(request.form['bhk'])
            bath = int(request.form['bath'])

        # Ensure location is provided
        if not location:
            return jsonify({'error': 'Location cannot be null or empty'}), 400

        # Get estimated price
        estimated_price = abc_1.get_estimated_price(location, total_sqft, bhk, bath)

        # Return the response
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    abc_1.load_saved_artifacts()
    app.run()