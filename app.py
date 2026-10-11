from math import isfinite, pi

from flask import Flask, jsonify, render_template, request
from linked_list import LinkedList
from stack import infix_to_postfix

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/linkedlist')
def linkedlist():
    return render_template('linkedlist.html')

@app.route('/stack')
def stack():
    return render_template('stack.html')

@app.route('/linkedlist/action', methods=['POST'])
def linkedlist_action():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error='Invalid request.'), 400

    values = payload.get('values')
    if (not isinstance(values, list) or len(values) > 50
            or any(not isinstance(value, str) or not value.strip() or len(value) > 24 for value in values)):
        return jsonify(error='The list must contain at most 50 values, each 1 to 24 characters long.'), 400

    linked_list = LinkedList()
    for value in values:
        linked_list.insert_at_end(value)

    action = payload.get('action')
    value = payload.get('value')
    target = payload.get('target')
    found_index = None

    if action in ('insert_at_beginning', 'insert_at_end', 'remove_at', 'search'):
        if not isinstance(value, str) or not value.strip() or len(value) > 24:
            return jsonify(error='Enter a value between 1 and 24 characters.'), 400

    if action in ('insert_at_beginning', 'insert_at_end', 'insert_after') and len(values) >= 50:
        return jsonify(error='The list can contain at most 50 nodes.'), 400

    if action == 'insert_at_beginning':
        linked_list.insert_at_beginning(value)
        message = f'Inserted {value} at the beginning.'
    elif action == 'insert_at_end':
        linked_list.insert_at_end(value)
        message = f'Inserted {value} at the end.'
    elif action == 'insert_after':
        if not isinstance(target, str) or not target.strip() or len(target) > 24:
            return jsonify(error='Enter the existing node value to insert after.'), 400
        if not isinstance(value, str) or not value.strip() or len(value) > 24:
            return jsonify(error='Enter a new value between 1 and 24 characters.'), 400
        if not linked_list.search(target):
            message = f'{target} is not in the list; nothing was inserted.'
        else:
            linked_list.insert_after(target, value)
            message = f'Inserted {value} after {target}.'
    elif action == 'search':
        if linked_list.search(value):
            found_index = values.index(value)
            message = f'Found {value} at node {found_index + 1}.'
        else:
            message = f'{value} is not in the list.'
    elif action == 'remove_beginning':
        removed = linked_list.remove_beginning()
        message = f'Removed {removed} from the beginning.' if removed is not None else 'The list is already empty.'
    elif action == 'remove_at_end':
        removed = linked_list.remove_at_end()
        message = f'Removed {removed} from the end.' if removed is not None else 'The list is already empty.'
    elif action == 'remove_at':
        removed = linked_list.remove_at(value)
        message = f'Removed the first {removed}.' if removed is not None else f'{value} is not in the list.'
    elif action == 'clear':
        linked_list = LinkedList()
        message = 'The list is empty.'
    else:
        return jsonify(error='Unknown linked-list action.'), 400

    updated_values = []
    current_node = linked_list.head
    while current_node:
        updated_values.append(current_node.data)
        current_node = current_node.next

    return jsonify(values=updated_values, message=message, found_index=found_index)

@app.route('/stack/convert', methods=['POST'])
def stack_convert():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error='Invalid request.'), 400

    expression = payload.get('expression')
    if not isinstance(expression, str) or len(expression) > 256:
        return jsonify(error='Enter an expression no longer than 256 characters.'), 400

    try:
        postfix, steps = infix_to_postfix(expression)
    except ValueError as error:
        return jsonify(error=str(error)), 400

    return jsonify(postfix=postfix, steps=steps)

@app.route('/uppercase', methods=['GET', 'POST'])
def uppercase():
    result = None
    if request.method == 'POST':
        result = request.form.get('inputString', '').upper()
    return render_template('touppercase.html', result=result)

@app.route('/circle', methods=['GET', 'POST'])
def circle():
    result = None
    error = None
    if request.method == 'POST':
        try:
            radius = float(request.form.get('radius', ''))
            if not isfinite(radius) or radius <= 0:
                raise ValueError
            result = f'{pi * radius ** 2:.2f}'
        except ValueError:
            error = 'Enter a number greater than zero.'
    return render_template('circle.html', result=result, error=error)

@app.route('/triangle', methods=['GET', 'POST'])
def triangle():
    result = None
    error = None
    if request.method == 'POST':
        try:
            base = float(request.form.get('base', ''))
            height = float(request.form.get('height', ''))
            if not isfinite(base) or not isfinite(height) or base <= 0 or height <= 0:
                raise ValueError
            result = f'{base * height / 2:.2f}'
        except ValueError:
            error = 'Enter a base and height greater than zero.'
    return render_template('triangle.html', result=result, error=error)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
