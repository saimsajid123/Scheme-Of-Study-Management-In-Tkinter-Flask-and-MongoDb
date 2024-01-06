# Sumbitted by:
# Muhammad Saim Sajid
# Rollno:
# F21BSEEN1E02025
# Semester:
# 5th
# Section:
# E1
# Sumbitted by:
# Huzaifa Qureshi
# Rollno:
# F21BSEEN1E02022
# Semester:
# 5th
# Section:
# E1
# Project:
# Scheme of Study Management In Tkinter
# Sumbitted To:
# Sir Nauman

# To install All The packages just type

# "pip install -r requirements.txt"

# in the terminal of vscode or whichever IDE you are Using

from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client['sos_database']
sos_collection = db['sos_collection']


@app.route('/sos', methods=['POST'])
def add_item():
    data = request.get_json()

    if 'subject_name' not in data or 'description' not in data or 'course_code' not in data or 'teacher_name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    selected_semester = data.get('selected_semester', 'Semester 1')
    course_info = f"{data['subject_name']}: {data['description']} ({data['course_code']}, {data['teacher_name']})"

    sos_collection.update_one({'semester': selected_semester}, {'$push': {'courses': course_info}}, upsert=True)

    return jsonify({'message': 'Item added successfully'}), 201


@app.route('/sos', methods=['GET'])
def get_items():
    selected_semester = request.args.get('selected_semester', 'Semester 1')

    result = sos_collection.find_one({'semester': selected_semester}, {'_id': 0, 'courses': 1})

    if result:
        return jsonify({'courses': result['courses']})
    else:
        return jsonify({'error': 'Semester not found'}), 404


@app.route('/sos', methods=['DELETE'])
def remove_item():
    selected_semester = request.args.get('selected_semester', 'Semester 1')
    selected_item = request.args.get('selected_item', '')

    if selected_item:
        sos_collection.update_one({'semester': selected_semester}, {'$pull': {'courses': selected_item}})
        return jsonify({'message': 'Item removed successfully'}), 200
    else:
        return jsonify({'error': 'Missing selected_item parameter'}), 400


if __name__ == "__main__":
    app.run(debug=True)
