from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

groups = [
    {
        "id": 1,
        "groupName": "Group 1",
        "members": [1, 2, 3],
    },
    {
        "id": 2,
        "groupName": "Group 2",
        "members": [4, 5],
    },
]

students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Eve"},
]

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    # TODO: (sample response below)
    return jsonify(groups)

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    # TODO: (sample response below)
    return jsonify(students)

@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object
    """
    
    # Getting the request body (DO NOT MODIFY)
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")
    
    # TODO: implement storage of a new group and return their info (sample response below)
    global groups
    global students
    new_id = 1
    members = []
    if groups:
        new_id = groups[-1]["id"] + 1
    for member_name in group_members:
        stu_id = -1
        for student in students:
            if student['name'] == member_name:
                stu_id = student['id']
                break
        if stu_id != -1 :
            members.append(stu_id)
        else:
            if students:
                stu_id = students[-1]['id'] + 1
                students.append({"id": stu_id, "name": member_name})
                members.append(stu_id)
            else:
                students.append({"id": 1, "name": member_name})
                members.append(1)
    groups.append({
        "id": new_id,
        "groupName": group_name,
        "members": members,
    })
    return jsonify({
        "id": new_id,
        "groupName": group_name,
        "members": members,
    }), 201

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    # TODO: (delete the group with the specified id)
    global groups
    groups = [group for group in groups if group["id"] != group_id]
    return '', 204  # Return 204 (do not modify this line)

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """
    # TODO: (sample response below)
    global groups
    global students
    group = [group for group in groups if group["id"] == group_id]
    if len(group) == 0:
        abort(404, "Group not found")
    members = []
    for stu_id in group[0]['members']:
        stu = [stu for stu in students if stu["id"] == stu_id][0]
        members.append(stu)
    return jsonify({
        "id": group[0]['id'],
        "groupName": group[0]['groupName'],
        "members": members,
    })
    # TODO:
    # if group id isn't valid:
    #     abort(404, "Group not found")

if __name__ == '__main__':
    app.run(port=3902, debug=True)
