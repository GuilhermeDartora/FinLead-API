from flask import jsonify

def success(message, data=None, status=200):
    response = {
        "success": True,
        "message": message
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status


def error(message, status=400):
    response = {
        "success": False,
        "message": message
    }

    return jsonify(response), status
