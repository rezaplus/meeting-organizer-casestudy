from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import logging
import bleach
from cerberus import Validator

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://mongo:27017/')
db = client.meeting_organizer
meetings_collection = db.meetings

# Set up logging
logging.basicConfig(filename='logs/meeting_organizer.log', level=logging.ERROR)

# Cerberus schema for validation
schema = {
    'subject': {'type': 'string', 'minlength': 1, 'maxlength': 255, 'required': True},
    'date': {'type': 'string', 'regex': r'\d{4}-\d{2}-\d{2}', 'required': True},
    'start_time': {'type': 'string', 'regex': r'\d{2}:\d{2}', 'required': True},
    'end_time': {'type': 'string', 'regex': r'\d{2}:\d{2}', 'required': True},
    'participants': {'type': 'string', 'minlength': 1, 'maxlength': 1024, 'required': True}
}
validator = Validator(schema)

def sanitize_meeting(meeting):
    """
    Sanitize meeting data by cleaning HTML and JavaScript from string fields.
    """
    for key, value in meeting.items():
        if isinstance(value, str):
            meeting[key] = bleach.clean(value)  # Clean string fields
    return meeting

@app.route('/api/meetings', methods=['POST'])
def create_meeting():
    """
    Create a new meeting.
    """
    try:
        meeting = request.json
        if not validator.validate(meeting):  # Validate input data
            return jsonify({'error': 'Invalid data', 'details': validator.errors}), 400
        
        meeting = sanitize_meeting(meeting)  # Sanitize input data
        meeting_id = meetings_collection.insert_one(meeting).inserted_id  # Insert meeting
        meeting['_id'] = str(meeting_id)
        return jsonify(meeting), 201
    except Exception as e:
        logging.error(f"Error in create_meeting: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/meetings', methods=['GET'])
def get_meetings():
    """
    Retrieve all meetings.
    """
    try:
        meetings = list(meetings_collection.find())  # Fetch all meetings
        for meeting in meetings:
            meeting['_id'] = str(meeting['_id'])
        return jsonify(meetings)
    except Exception as e:
        logging.error(f"Error in get_meetings: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/meetings/<id>', methods=['GET'])
def get_meeting(id):
    """
    Retrieve a single meeting by ID.
    """
    try:
        meeting = meetings_collection.find_one({'_id': ObjectId(id)})  # Fetch meeting by ID
        if meeting:
            meeting['_id'] = str(meeting['_id'])
            return jsonify(meeting)
        else:
            return jsonify({'error': 'Meeting not found'}), 404
    except Exception as e:
        logging.error(f"Error in get_meeting: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/meetings/<id>', methods=['PUT'])
def update_meeting(id):
    """
    Update an existing meeting by ID.
    """
    try:
        meeting = request.json
        if not validator.validate(meeting):  # Validate input data
            return jsonify({'error': 'Invalid data', 'details': validator.errors}), 400
        
        meeting = sanitize_meeting(meeting)  # Sanitize input data
        result = meetings_collection.update_one({'_id': ObjectId(id)}, {'$set': meeting})  # Update meeting
        if result.matched_count:
            meeting['_id'] = id
            return jsonify(meeting)
        else:
            return jsonify({'error': 'Meeting not found'}), 404
    except Exception as e:
        logging.error(f"Error in update_meeting: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/meetings/<id>', methods=['DELETE'])
def delete_meeting(id):
    """
    Delete a meeting by ID.
    """
    try:
        result = meetings_collection.delete_one({'_id': ObjectId(id)})  # Delete meeting by ID
        if result.deleted_count:
            return '', 204
        else:
            return jsonify({'error': 'Meeting not found'}), 404
    except Exception as e:
        logging.error(f"Error in delete_meeting: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the app
