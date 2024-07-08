from better_profanity import profanity
from flask import jsonify

import databaseManagement

# Load the default list of profane words for censorship
profanity.load_censor_words()

# Function to censor profanity in the content
def censorContent(content):
    return profanity.censor(content)

# Function to check if content has profane words
def containsProfanity(content):
    censoredContent = censorContent(content)
    return content != censoredContent

# Function to handle incoming request data and sanitize it
def sanitizeInput(data, key):
    sanitizedData = {}
    value = data.get(key, '').lower()
    if containsProfanity(value):
        return None
    sanitizedData[key] = value
    return sanitizedData

# Function to check data information for disallowed words
def containsDisallowedWords(content):
    # List of disallowed words
    disallowedWords = ['apple', 'orange', 'banana', 'spinach', 'broccoli', 'pumpkin', 'pineapple']
    # Check if any disallowed word is present in food
    # if any(food in word for word in disallowedWords):
    if content in disallowedWords:
        return True
    else:
        return False

# Function to check if orderItem is on the menu
def isItemOnMenu(orderItem):
    databaseResults = databaseManagement.getOnlyMenuItems()
    menuItems = []
    for databaseResult in databaseResults:
        menuItems.append(databaseResult.get('menuitem', '').lower())
    if orderItem in menuItems:
        return True
    return False

# Function to check if details are allowed
def isOrderDetailAllowed(detailCategory, orderItem, orderDetail):
    databaseResults = databaseManagement.getMenuItemsDetails(detailCategory, orderItem)
    strAllowedDetails = databaseResults[0].get(str(detailCategory), '')
    allowedDetails = strAllowedDetails.split(', ')
    if orderDetail in allowedDetails:
        return True
    else:
        return False

def validateOrderDetails(orderItem, flavor, size, temp):
    if not isItemOnMenu(orderItem):
        return jsonify({'message': 'Invalid input - orderItem: \'' + orderItem + '\' not on menu.'})
    elif not isOrderDetailAllowed('flavor', orderItem, flavor):
        return jsonify({'message': 'Invalid input - orderDetail: \'' + flavor + '\' not a flavor for ' + orderItem + '.'})
    elif not isOrderDetailAllowed('size', orderItem, size):
        return jsonify({'message': 'Invalid input - orderDetail: \'' + size + '\' not a size for ' + orderItem + '.'})
    elif not isOrderDetailAllowed('temperature', orderItem, temp):
        return jsonify({'message': 'Invalid input - orderDetail: \'' + temp + '\' not a temp for ' + orderItem + '.'})
    else:
        return None
    
# Function to pull order details from data and sanitize
def sanitizeNewOrder(data):
    orderInfos = ['orderItem', 'flavor', 'size', 'temp']
    sanitizedOrderInfo = []
    for orderInfo in orderInfos:
        tempValue = data.get(orderInfo, '')
        if containsProfanity(tempValue):
            return None, None, None, None
        sanitizedOrderInfo.append(tempValue.lower())
    return sanitizedOrderInfo[0], sanitizedOrderInfo[1], sanitizedOrderInfo[2], sanitizedOrderInfo[3]

#Function to validate this is an existing order number
def isOrderNumberInDatabase(orderNumber):
    databaseResults = databaseManagement.getOnlyOrderIds()
    orderIds = []
    for databaseResult in databaseResults:
        orderIds.append(databaseResult.get('orderid', ''))
    if orderNumber in orderIds:
        return True
    return False

# Function to pull order details from data and sanitize
def sanitizeExistingOrder(data):
    orderInfos = ['orderNumber', 'status']
    sanitizedOrderInfo = []
    for orderInfo in orderInfos:
        tempValue = data.get(orderInfo, '')
        if containsProfanity(tempValue):
            return None, None
        sanitizedOrderInfo.append(tempValue)
    return sanitizedOrderInfo[0], sanitizedOrderInfo[1]