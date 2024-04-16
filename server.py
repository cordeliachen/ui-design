from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# Load your dataset
with open('dataset.json') as f:
    data = json.load(f)

@app.route('/')
def index():
    # Show 3 popular items dynamically
    popular_items = list(data.values())[:3]
    return render_template('index.html', items=popular_items)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['search'].lower()
    else:
        # Look for both 'query' and 'specialty' parameters, defaulting to an empty string if neither is found
        query = request.args.get('query', default='').lower() or request.args.get('specialty', default='').lower()

    matching_results = []
    for item in data.values():
        if query in item['name'].lower() or query in item['Location'].lower() or any(query in specialty.lower() for specialty in item['Specialties']):
            matching_results.append(item)

    num_results = len(matching_results)
    return render_template('search_results.html', items=matching_results, query=query, num_results=num_results)


@app.route('/view/<id>')
def view_item(id):
    item = data.get(id, None)
    if item:
        return render_template('view_item.html', item=item)
    return 'Item not found', 404

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            # Add validation checks here, if necessary
            new_id = str(max([int(x) for x in data.keys()], default=0) + 1)
            new_item = {
                'id': new_id,
                'name': request.form['name'],
                'image_url': request.form['image_url'],
                'description': request.form['description'],
                'rating': int(request.form['rating']),
                'Famous_alumni': request.form['famous_alumni'].split(','),
                'Specialties': request.form['specialties'].split(','),
                'Location': request.form['location']
            }
            # More validation can be performed here
            if not new_item['name'].strip():
                raise ValueError('The name field is required.')
            if int(new_item['rating']) not in range(1, 6):
                raise ValueError('Rating must be between 1 and 5.')
            # ... more validation as needed ...

            data[new_id] = new_item
            with open('dataset.json', 'w') as f:
                json.dump(data, f, indent=4)
            return jsonify({'success': True, 'id': new_id})
        except Exception as e:
            return jsonify({'success': False, 'error': 'Failed to add the item: ' + str(e)})
    else:
        return render_template('add_item.html')



@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_item(id):
    item = data.get(id, None)
    if not item:
        return 'Item not found', 404
    if request.method == 'POST':
        item['name'] = request.form['name']
        item['image_url'] = request.form['image_url']
        item['description'] = request.form['description']
        item['rating'] = request.form['rating']
        item['Famous_alumni'] = request.form.get('famous_alumni').split(', ')
        item['Specialties'] = request.form.get('specialties').split(', ')
        item['Location'] = request.form['location']
        with open('dataset.json', 'w') as f:
            json.dump(data, f)
        return redirect(url_for('view_item', id=id))
    else:
        return render_template('edit_item.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)
