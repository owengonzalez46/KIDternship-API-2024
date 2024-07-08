from flask import Flask, request, jsonify, send_file, Response
from logging.handlers import RotatingFileHandler
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import wordcloudManagement
import databaseManagement
import dataSanitization
import fileOperations
import logging
import random

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
socketio = SocketIO(app, cors_allowed_origins="*")  # Initialize Socket.IO with CORS support

# Configure logging
logHandler = RotatingFileHandler('posts.log', maxBytes=10000, backupCount=1)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
app.logger.addHandler(logHandler)
app.logger.setLevel(logging.INFO)

# Pass the logger to fileOperations
fileOperations.initLogger(app.logger)

# Root route to provide basic information
@app.route('/')
def index():
    return 'Welcome to the API!'

###################################################### Wordcloud Resources ######################################################

# Route to handle adding a new word to the wordcloud
@app.route('/wordcloud/words', methods=['POST'])
def addWordToCloud():
    if request.is_json:
        data = request.get_json()
        sanitizedData = dataSanitization.sanitizeInput(data, 'word')       
        if sanitizedData is None:
            return jsonify({'message': 'Input contains profane language and cannot be accepted.'}), 400
        
        if databaseManagement.insertWordIntoCloud(sanitizedData):
            fileOperations.logAndAppend('/wordcloud', sanitizedData)
            return jsonify({'message': 'Word(s) added to wordcloud!'}), 200
        else:
            return jsonify({'message': 'Failed to post'}), 500        
    else:
        return jsonify({'message': 'Invalid input, expected JSON'}), 400

# Route to generate and return the wordcloud    
@app.route('/wordcloud/display', methods=['GET'])
def generateWordcloud():
    img = wordcloudManagement.generateWordcloud()
    if img:
        return send_file(img, mimetype='image/png')
    else:
        return Response("No words found in the database.", status=404)

###################################################### Introductory Resources ######################################################

# Root route to return Hello World
@app.route('/introduction/hello-world', methods=['GET'])
def helloWorld():
    return jsonify({'message': 'Hello World!'})

# Root route to take in a user's name and return a user id
@app.route('/introduction/user-id/<username>', methods=['GET'])
def userId(username):
    if dataSanitization.containsProfanity(username):
        return jsonify({'message': 'Input contains profane language and cannot be accepted.'}), 400
    userId = username.lower() + '-' + str(random.randrange(1000,2000))
    fileOperations.logAndAppend("/introduction/user-id", userId)
    return jsonify({'message': 'Hello ' + username + '. Your userId is ' + userId})

# Route to take in a food and return if it is allowed or not
@app.route('/introduction/food', methods=['POST'])
def post():
    if request.is_json:
        data = request.get_json()
        sanitizedData = dataSanitization.sanitizeInput(data, 'food')
        
        if sanitizedData is None:
            return jsonify({'message': 'Post contains profane language'}), 400

        fileOperations.logAndAppend("/introduction/food", sanitizedData)

        food = sanitizedData.get('food', '').lower()

        if dataSanitization.containsDisallowedWords(food):
            return jsonify({'message': 'Content contains disallowed words. Disallowed word: ' + food}), 400
        else:
            return jsonify({'message': 'Content doesn\'t contain disallowed words. Allowed word: ' + food}), 200
    else:
        return jsonify({'message': 'Invalid input, expected JSON'}), 400

###################################################### Bakery Resources ######################################################

# Route to return menu items
@app.route('/bakery/menu', methods=['GET'])
def getMenuItems():
    products = databaseManagement.getAllMenuItems()
    if products is not None:
        return jsonify(products)
    else:
        return jsonify({'message': 'No items found.'}), 404

# Route to return menu items for a given category
@app.route('/bakery/menu/<category>', methods=['GET'])
def getMenuItemsWithCategory(category):
    if dataSanitization.containsProfanity(category):
        return jsonify({'message': 'Input contains profane language and cannot be accepted.'}), 400
    fileOperations.logAndAppend("/bakery/menu/<category>", category)
    products = databaseManagement.getAllMenuItemsForCategory(category)
    if products is not None:
        return jsonify(products)
    else:
        return jsonify({'message': 'No items found for the category: ' + category + "."}), 404

# Route to show the orders in the database
@app.route('/bakery/orders', methods=['GET'])
def getOrders():
    products = databaseManagement.getAllOrders()
    if products is not None:
        return jsonify(products)
    else:
        return jsonify({'message': 'No orders found.'}), 404

# Route to show the orders in the database
@app.route('/bakery/orders', methods=['POST'])
def insertOrder():
    if request.is_json:
        data = request.get_json()
        orderItem, flavor, size, temp = dataSanitization.sanitizeNewOrder(data)
        orderString = str(orderItem) + '| ' + str(flavor) + '| ' + str(size) + '| ' + str(temp)
        if orderItem is None:
            return jsonify({'message': 'Post contains profane language'}), 400
        fileOperations.logAndAppend("/bakery/orders", orderString)
        validateOrderDetailsResponse = dataSanitization.validateOrderDetails(orderItem, flavor, size, temp)
        if not validateOrderDetailsResponse is None:
            return validateOrderDetailsResponse, 400
        orderId, inputSuccessful = databaseManagement.insertOrder(orderItem, flavor, size, temp)
        if inputSuccessful:
            return jsonify({'message': 'Successfully inserted order into database. Order Number: ' + orderId})
        else:
            return jsonify({'message': 'Unable to insert order ' + orderId + ' into database.'})
    else:
        return jsonify({'message': 'Invalid input, expected JSON'}), 400

# Route to show the orders in the database
@app.route('/bakery/orders/<orderNumber>', methods=['GET'])
def getSpecificOrder(orderNumber):
    if dataSanitization.containsProfanity(orderNumber):
        return jsonify({'message': 'Input contains profane language and cannot be accepted.'}), 400
    fileOperations.logAndAppend("/bakery/orders/<orderNumber>", orderNumber)
    order = databaseManagement.getSpecificOrder(orderNumber)
    if order is not None:
            return jsonify(order)
    else:
        return jsonify({'message': 'No order found for order number: ' + str(orderNumber)}), 404
    
# Route to show the orders in the database
@app.route('/bakery/orders', methods=['PUT'])
def updateOrder():
    data = request.get_json()
    orderNumber, status = dataSanitization.sanitizeExistingOrder(data)
    if orderNumber is None:
        return jsonify({'message': 'Post contains profane language'}), 400
    fileOperations.logAndAppend("/bakery/orders", orderNumber)
    if not dataSanitization.isOrderNumberInDatabase(orderNumber):
        return jsonify({'message': 'Order number: \'' + orderNumber + '\' does not exist.'}), 400
    updateStatus = databaseManagement.updateOrder(orderNumber, status)
    if updateStatus:
        return jsonify({'message': 'Updated order number: ' + orderNumber})
    else:
        return jsonify({'message': 'Unable to update order number: ' + orderNumber})

# Main entry point to run the Flask app with Socket.IO support
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True, allow_unsafe_werkzeug=True)
