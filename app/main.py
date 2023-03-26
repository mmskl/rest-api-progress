from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from main import User, Progress, Podcast, Queue, Subscription

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Swagger(app)


@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    tags:
      - User
    responses:
      200:
        description: List of all users
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                description: The user ID
              name:
                type: string
                description: The user's name
              email:
                type: string
                description: The user's email address
    """
    users = User.query.all()
    result = []
    for user in users:
        result.append({'id': user.id, 'name': user.name, 'email': user.email})
    return jsonify(result)

@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            name:
              type: string
              description: The user's name
            email:
              type: string
              description: The user's email address
    responses:
      200:
        description: User created successfully
    """
    name = request.json['name']
    email = request.json['email']
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        description: The ID of the user to get
        required: true
        type: integer
    responses:
      200:
        description: The user with the specified ID
        schema:
          properties:
            id:
              type: integer
              description: The user ID
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            name:
              type: string
              description: The name of the user
              example: John Doe
            email:
              type: string
              description: The email address of the user
              example: john.doe@example.com
    """
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    user_data = {'id': user.id, 'name': user.name, 'email': user.email}
    return jsonify(user_data)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user by ID
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        description: The ID of the user to update
        required: true
        type: integer
      - name: name
        in: formData
        description: The name of the user
        required: true
        type: string
      - name: email
        in: formData
        description: The email address of the user
        required: true
        type: string
    responses:
      200:
        description: The updated user
        schema:
          properties:
            id:
              type: integer
              description: The user ID
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            name:
              type: string
              description: The name of the user
              example: John Doe
            email:
              type: string
              description: The email address of the user
              example: john.doe@example.com
    """
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    name = request.form['name']
    email = request.form['email']
    user.name = name
    user.email = email
    db.session.commit()
    user_data = {'id': user.id, 'name': user.name, 'email': user.email}
    return jsonify(user_data)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete user by ID
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        description: The ID of the user to delete
        required: true
        type: integer
    responses:
      200:
        description: The message confirming deletion
    """
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})



@app.route('/progress', methods=['GET'])
def get_all_progress():
    """
    Get all progress
    ---
    tags:
      - Progress
    responses:
      200:
        description: All progress
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                description: The progress ID
                example: 1
                readOnly: true
                format: int64
                minimum: 1
              user_id:
                type: integer
                description: The ID of the user who made the progress
                example: 1
                readOnly: true
                format: int64
                minimum: 1
              podcast_id:
                type: integer
                description: The ID of the podcast for which progress was made
                example: 1
                readOnly: true
                format: int64
                minimum: 1
              progress:
                type: integer
                description: The progress made in the podcast
                example: 30
                minimum: 0
                maximum: 100
    """
    progress = Progress.query.all()
    progress_data = []
    for prog in progress:
        prog_data = {'id': prog.id, 'user_id': prog.user_id,
                     'podcast_id': prog.podcast_id, 'progress': prog.progress}
        progress_data.append(prog_data)
    return jsonify(progress_data)


@app.route('/progress/<int:progress_id>', methods=['GET'])
def get_progress(progress_id):
    """
    Get progress by ID
    ---
    tags:
      - Progress
    parameters:
      - name: progress_id
        in: path
        description: The ID of the progress to get
        required: true
        type: integer
    responses:
      200:
        description: The progress with the specified ID
        schema:
          properties:
            id:
              type: integer
              description: The progress ID
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            user_id:
              type: integer
              description: The ID of the user who made the progress
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            podcast_id:
              type: integer
              description: The ID of the podcast for which progress was made
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            progress:
              type: integer
              description: The progress made in the podcast
              example: 30
              minimum: 0
              maximum: 100
    """
    prog = Progress.query.get(progress_id)
    if prog is None:
        return jsonify({'message': 'Progress not found'}), 404
    prog_data = {'id': prog.id, 'user_id': prog.user_id,
                 'podcast_id': prog.podcast_id, 'progress': prog.progress}
    return jsonify(prog_data)

@app.route('/progress/<int:user_id>/<int:podcast_id>', methods=['GET'])
def get_progress_by_user_and_podcast(user_id, podcast_id):
    """
    Get progress for a specific podcast and user
    ---
    tags:
      - Progress
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user whose progress is being requested
      - name: podcast_id
        in: path
        type: integer
        required: true
        description: The ID of the podcast for which progress is being requested
    responses:
      200:
        description: The progress was found successfully
        schema:
          $ref: '#/definitions/Progress'
      404:
        description: The progress was not found
    """

    user_id = get_user_id()
    progress = Progress.query.filter_by(user_id=user_id, podcast_id=podcast_id).first()
    if progress:
        return jsonify(progress.serialize()), 200
    else:
        abort(404)




@app.route('/progress', methods=['POST'])
def create_progress():
    """
    Create new progress
    ---
    tags:
      - Progress
    parameters:
      - name: user_id
        in: formData
        description: The ID of the user who made the progress
        required: true
        type: integer
      - name: podcast_id
        in: formData
        description: The ID of the podcast for which progress was made
        required: true
        type: integer
      - name: progress
        in: formData
        description: The progress made in the podcast
        required: true
        type: integer
    responses:
      201:
        description: The newly created progress
        schema:
          properties:
            id:
              type: integer
              description: The progress ID
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            user_id:
              type: integer
              description: The ID of the user who made the progress
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            podcast_id:
              type: integer
              description: The ID of the podcast for which progress was made
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            progress:
              type: integer
              description: The progress made in the podcast
              example: 30
              minimum: 0
              maximum: 100
    """
    user_id = request.form.get('user_id')
    podcast_id = request.form.get('podcast_id')
    progress = request.form.get('progress')

    if not user_id or not podcast_id or not progress:
        return jsonify({'message': 'Please provide all required fields.'}), 400

    # Check if user and podcast exist
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    podcast = Podcast.query.get(podcast_id)
    if podcast is None:
        return jsonify({'message': 'Podcast not found'}), 404

    # Create new progress
    new_progress = Progress(user_id=user_id, podcast_id=podcast_id, progress=progress)
    db.session.add(new_progress)
    db.session.commit()

    prog_data = {'id': new_progress.id, 'user_id': new_progress.user_id,
                 'podcast_id': new_progress.podcast_id, 'progress': new_progress.progress}
    return jsonify(prog_data), 201



@app.route('/progress/<int:user_id>/<int:podcast_id>', methods=['PUT'])
def update_progress(progress_id):
    """
    Update progress by ID
    ---
    tags:
      - Progress
    parameters:
      - name: progress_id
        in: path
        description: The ID of the progress to update
        required: true
        type: integer
      - name: user_id
        in: formData
        description: The ID of the user who made the progress
        type: integer
      - name: podcast_id
        in: formData
        description: The ID of the podcast for which progress was made
        type: integer
      - name: progress
        in: formData
        description: The progress made in the podcast
        type: integer
    responses:
      200:
        description: The updated progress
        schema:
          properties:
            id:
              type: integer
              description: The progress ID
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            user_id:
              type: integer
              description: The ID of the user who made the progress
              example: 1
              format: int64
              minimum: 1
            podcast_id:
              type: integer
              description: The ID of the podcast for which progress was made
              example: 1
              format: int64
              minimum: 1
            progress:
              type: integer
              description: The progress made in the podcast
              example: 30
              minimum: 0
              maximum: 100
      404:
        description: Progress not found
    """


    progress = Progress.query.filter_by(user_id=user_id, podcast_id=podcast_id).first()
    if progress is None:
        return jsonify({'message': 'Progress not found.'}), 404

    time = request.json.get('time', progress.time)
    progress.time = time
    db.session.commit()

    # # Check if user and podcast exist
    # user = User.query.get(user_id)
    # if user is None:
    #     return jsonify({'message': 'User not found'}), 404
    # podcast = Podcast.query.get(podcast_id)
    # if podcast is None:
    #     return jsonify({'message': 'Podcast not found'}), 404
    #
    # progress.user_id = user_id
    # progress.podcast_id = podcast_id
    # progress.progress = progress_val
    # db.session.commit()

    prog_data = {'id': progress.id, 'user_id': progress.user_id,
                 'podcast_id': progress.podcast_id, 'progress': progress.progress}
    return jsonify(prog_data), 200


@app.route('/progress/<int:progress_id>', methods=['DELETE'])
def delete_progress(progress_id):
    """
    Delete progress by ID
    ---
    tags:
      - Progress
    parameters:
      - name: progress_id
        in: path
        description: The ID of the progress to delete
        required: true
        type: integer
    responses:
      204:
        description: Progress deleted successfully
      404:
        description: Progress not found
    """
    progress = Progress.query.get(progress_id)
    if progress is None:
        return jsonify({'message': 'Progress not found'}), 404

    db.session.delete(progress)
    db.session.commit()

    return '', 204




@app.route('/podcasts', methods=['GET'])
def get_podcasts():
    """
    Get all podcasts
    ---
    tags:
      - podcasts
    responses:
      200:
        description: A list of all podcasts
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                description: The podcast ID
                example: 1
                readOnly: true
                format: int64
                minimum: 1
              name:
                type: string
                description: The podcast name
                example: 'My Podcast'
              author_id:
                type: integer
                description: The ID of the author of the podcast
                example: 1
                format: int64
                minimum: 1
              description:
                type: string
                description: The podcast description
                example: 'A podcast about technology'
              created_at:
                type: string
                description: The timestamp when the podcast was created
                example: '2022-03-01T10:30:00Z'
                format: date-time
    """
    podcasts = Podcast.query.all()
    podcasts_data = [{'id': podcast.id, 'name': podcast.name,
                      'author_id': podcast.author_id, 'description': podcast.description,
                      'created_at': podcast.created_at.isoformat()}
                     for podcast in podcasts]
    return jsonify(podcasts_data), 200


@app.route('/podcasts/<int:podcast_id>', methods=['GET'])
def get_podcast(podcast_id):
    """
    Get podcast by ID
    ---
    tags:
      - podcasts
    parameters:
      - name: podcast_id
        in: path
        description: The ID of the podcast to get
        required: true
        type: integer
    responses:
      200:
        description: The podcast with the given ID
        schema:
          properties:
            id:
              type: integer
              description: The podcast ID
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            name:
              type: string
              description: The podcast name
              example: 'My Podcast'
            author_id:
              type: integer
              description: The ID of the author of the podcast
              example: 1
              format: int64
              minimum: 1
            description:
              type: string
              description: The podcast description
              example: 'A podcast about technology'
            created_at:
              type: string
              description: The timestamp when the podcast was created
              example: '2022-03-01T10:30:00Z'
              format: date-time
      404:
        description: Podcast not found
    """
    podcast = Podcast.query.get(podcast_id)
    if podcast is None:
        return jsonify({'message': 'Podcast not found'}), 404

    podcast_data = {'id': podcast.id, 'name': podcast.name,
                    'author_id': podcast.author_id, 'description': podcast.description,
                    'created_at': podcast.created_at.isoformat()}
    return jsonify(podcast_data), 200



@app.route('/podcasts', methods=['POST'])
def create_podcast():
    """
    Create a new podcast
    ---
    tags:
      - podcasts
    parameters:
      - name: name
        in: formData
        description: The name of the podcast
        required: true
        type: string
      - name: author_id
        in: formData
        description: The ID of the author of the podcast
        required: true
        type: integer
      - name: description
        in: formData
        description: The description of the podcast
        required: true
        type: string
    responses:
      201:
        description: The newly created podcast
        schema:
          properties:
            id:
              type: integer
              description: The podcast ID
              example: 1
              readOnly: true
              format: int64
              minimum: 1
            name:
              type: string
              description: The podcast name
              example: 'My Podcast'
            author_id:
              type: integer
              description: The ID of the author of the podcast
              example: 1
              format: int64
              minimum: 1
            description:
              type: string
              description: The podcast description
              example: 'A podcast about technology'
            created_at:
              type: string
              description: The timestamp when the podcast was created
              example: '2022-03-01T10:30:00Z'
              format: date-time
    """
    name = request.form.get('name')
    author_id = request.form.get('author_id')
    description = request.form.get('description')

    if not name or not author_id or not description:
        return jsonify({'message': 'Missing required parameters'}), 400

    try:
        podcast = Podcast(name=name, author_id=author_id, description=description)
        db.session.add(podcast)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating podcast: {str(e)}'}), 500

    podcast_data = {'id': podcast.id, 'name': podcast.name,
                    'author_id': podcast.author_id, 'description': podcast.description,
                    'created_at': podcast.created_at.isoformat()}
    return jsonify(podcast_data), 201

@app.route('/podcasts/<int:podcast_id>', methods=['PUT'])
def update_podcast(podcast_id):
    """
    Update a specific podcast
    ---
    tags:
      - podcasts
    parameters:
      - name: podcast_id
        in: path
        type: integer
        required: true
        description: The ID of the podcast to update
      - name: name
        in: query
        type: string
        required: true
        description: The new name of the podcast
      - name: author_id
        in: query
        type: integer
        required: true
        description: The ID of the author of the podcast
    responses:
      200:
        description: The updated podcast
        schema:
          id: Podcast
          properties:
            id:
              type: integer
              description: The ID of the podcast
            name:
              type: string
              description: The name of the podcast
            author_id:
              type: integer
              description: The ID of the author of the podcast
      404:
        description: Podcast not found
    """
    podcast = Podcast.query.get(podcast_id)
    if not podcast:
        return jsonify({'error': 'Podcast not found'}), 404

    name = request.args.get('name')
    author_id = request.args.get('author_id')

    if not name and not author_id:
        return jsonify({'error': 'At least one parameter must be provided'}), 400

    if name:
        podcast.name = name

    if author_id:
        author = Author.query.get(author_id)
        if not author:
            return jsonify({'error': 'Author not found'}), 404
        podcast.author_id = author_id

    db.session.commit()

    return jsonify({'id': podcast.id, 'name': podcast.name, 'author_id': podcast.author_id})


@app.route('/podcasts/<int:podcast_id>', methods=['DELETE'])
def delete_podcast(podcast_id):
    """
    Delete a specific podcast
    ---
    tags:
      - podcasts
    parameters:
      - name: podcast_id
        in: path
        type: integer
        required: true
        description: The ID of the podcast to delete
    responses:
      200:
        description: Podcast deleted successfully
      404:
        description: Podcast not found
    """
    podcast = Podcast.query.get(podcast_id)
    if not podcast:
        return jsonify({'error': 'Podcast not found'}), 404

    db.session.delete(podcast)
    db.session.commit()

    return jsonify({'message': 'Podcast deleted successfully'})




@app.route('/authors', methods=['POST'])
def create_author():
    """
    Create a new author

    ---
    tags:
      - authors
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: The name of the author
      - name: email
        in: query
        type: string
        required: true
        description: The email address of the author
    responses:
      201:
        description: The newly created author
        schema:
          id: Author
          properties:
            id:
              type: integer
              description: The ID of the author
            name:
              type: string
              description: The name of the author
            email:
              type: string
              description: The email address of the author
    """
    name = request.args.get('name')
    email = request.args.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email must be provided'}), 400

    author = Author(name=name, email=email)
    db.session.add(author)
    db.session.commit()

    return jsonify({'id': author.id, 'name': author.name, 'email': author.email}), 201

@app.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    """
    Get a specific author by ID

    ---
    tags:
      - authors
    parameters:
      - name: author_id
        in: path
        type: integer
        required: true
        description: The ID of the author to retrieve
    responses:
      200:
        description: The requested author
        schema:
          id: Author
          properties:
            id:
              type: integer
              description: The ID of the author
            name:
              type: string
              description: The name of the author
            email:
              type: string
              description: The email address of the author
      404:
        description: Author not found
    """
    author = Author.query.get(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404

    return jsonify({'id': author.id, 'name': author.name, 'email': author.email})



@app.route('/authors', methods=['GET'])
def get_authors():
    """
    Get all authors
    ---
    tags:
      - authors
    responses:
      200:
        description: A list of authors
        schema:
          type: array
          items:
            $ref: '#/definitions/Author'
    """
    authors = Author.query.all()
    return jsonify([author.serialize() for author in authors]), 200



@app.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    """
    Update an existing author
    ---
    tags:
      - authors
    parameters:
      - in: path
        name: author_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/UpdateAuthor'
    responses:
      200:
        description: Updated author
        schema:
          $ref: '#/definitions/Author'
      404:
        description: Author not found
    """
    author = Author.query.get(author_id)
    if not author:
        return jsonify({'message': 'Author not found'}), 404

    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Name is required'}), 400

    author.name = name
    db.session.commit()
    return jsonify(author.serialize()), 200


@app.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    """
    Delete an author
    ---
    tags:
      - authors
    parameters:
      - in: path
        name: author_id
        type: integer
        required: true
    responses:
      204:
        description: Author deleted
      404:
        description: Author not found
    """
    author = Author.query.get(author_id)
    if not author:
        return jsonify({'message': 'Author not found'}), 404

    db.session.delete(author)
    db.session.commit()
    return '', 204




@app.route('/queue', methods=['GET'])
def get_queue():
    """
    Retrieve all podcasts in the queue
    ---
    tags:
      - Queue
    responses:
      200:
        description: A list of podcasts in the queue
        schema:
          type: array
          items:
            $ref: '#/definitions/Queue'
    """
    queue = Queue.query.all()
    result = queues_schema.dump(queue)
    return jsonify(result)







@app.route('/queue', methods=['POST'])
def add_to_queue():
    """
    Add a podcast to the queue
    ---
    tags:
      - Queue
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/QueueInput'
    responses:
      201:
        description: Successfully added podcast to the queue
        schema:
          $ref: '#/definitions/Queue'
      400:
        description: Bad request - invalid input
    """
    data = request.get_json()
    new_podcast = Queue(name=data['name'], description=data['description'], author=data['author'], audio_link=data['audio_link'])
    db.session.add(new_podcast)
    db.session.commit()
    result = queue_schema.dump(new_podcast)
    return jsonify(result), 201

@app.route('/queue/<int:queue_id>', methods=['PUT'])
def update_queue(queue_id):
    """
    Update a podcast in the queue
    ---
    tags:
      - Queue
    parameters:
      - name: queue_id
        in: path
        required: true
        description: ID of the podcast in the queue to update
        type: integer
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/QueueInput'
    responses:
      200:
        description: Successfully updated podcast in the queue
        schema:
          $ref: '#/definitions/Queue'
      400:
        description: Bad request - invalid input
      404:
        description: Podcast in queue not found
    """
    data = request.get_json()
    podcast = Queue.query.get(queue_id)
    if not podcast:
        return jsonify({'message': 'Podcast not found in queue'}), 404
    podcast.name = data['name']
    podcast.description = data['description']
    podcast.author = data['author']
    podcast.audio_link = data['audio_link']
    db.session.commit()
    result = queue_schema.dump(podcast)
    return jsonify(result)


@app.route('/queue/<int:queue_id>', methods=['DELETE'])
def delete_queue(queue_id):
    """
    Delete a queue item by ID
    ---
    tags:
      - Queue
    parameters:
      - name: queue_id
        in: path
        type: integer
        required: true
        description: The ID of the queue item to delete
    responses:
      204:
        description: The queue item was deleted successfully
      404:
        description: The queue item was not found
    """
    queue_item = Queue.query.filter_by(id=queue_id).first()
    if queue_item:
        db.session.delete(queue_item)
        db.session.commit()
        return '', 204
    else:
        abort(404)



@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    """
    Get all subscriptions

    Returns:
    List of dictionaries with subscription details
    ---
    tags:
      - Subscription
    responses:
        200:
            description: List of subscriptions
            schema:
                type: array
                items:
                    $ref: '#/definitions/Subscription'
    """
    subscriptions = Subscription.query.all()
    return jsonify([s.to_dict() for s in subscriptions])


@app.route('/subscriptions', methods=['POST'])
def add_subscription():
    """
    Add a new subscription
    ---
    tags:
      - Subscription
    parameters:
        - in: body
          name: body
          schema:
            $ref: '#/definitions/Subscription'
    responses:
        201:
            description: Details of newly added subscription
            schema:
                $ref: '#/definitions/Subscription'
    """
    data = request.get_json()
    subscription = Subscription(**data)
    db.session.add(subscription)
    db.session.commit()
    return jsonify(subscription.to_dict()), 201


@app.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    """
    Update a subscription by ID.
    ---
    tags:
      - Subscription
    parameters:
      - name: subscription_id
        in: path
        type: integer
        required: true
        description: ID of the subscription to update
      - name: title
        in: formData
        type: string
        required: false
        description: New title of the subscription
      - name: description
        in: formData
        type: string
        required: false
        description: New description of the subscription
      - name: language
        in: formData
        type: string
        required: false
        description: New language of the subscription
      - name: pubDate
        in: formData
        type: string
        required: false
        description: New pubDate of the subscription
      - name: image_url
        in: formData
        type: string
        required: false
        description: New image URL of the subscription
      - name: url
        in: formData
        type: string
        required: false
        description: New URL of the subscription
      - name: author_name
        in: formData
        type: string
        required: false
        description: New author name of the subscription
    security:
      - Bearer: []
    responses:
      200:
        description: Subscription updated successfully
      404:
        description: Subscription not found
    """
    subscription = Subscription.query.get_or_404(subscription_id)

    title = request.form.get('title')
    description = request.form.get('description')
    language = request.form.get('language')
    pubDate = request.form.get('pubDate')
    image_url = request.form.get('image_url')
    url = request.form.get('url')
    author_name = request.form.get('author_name')

    if title:
        subscription.title = title
    if description:
        subscription.description = description
    if language:
        subscription.language = language
    if pubDate:
        subscription.pubDate = pubDate
    if image_url:
        subscription.image_url = image_url
    if url:
        subscription.url = url
    if author_name:
        subscription.author_name = author_name

    db.session.commit()

    return jsonify({'message': 'Subscription updated successfully'})


# GET a specific subscription
@app.route('/subscriptions/<int:subscription_id>', methods=['GET'])
def get_subscription(subscription_id):
    """
    Get details about a specific subscription.
    ---
    tags:
      - Subscription
    parameters:
      - name: subscription_id
        in: path
        type: integer
        required: true
        description: ID of the subscription to get
    responses:
      200:
        description: A subscription object
        schema:
          $ref: '#/definitions/Subscription'
      404:
        description: Subscription not found
    """
    subscription = Subscription.query.get_or_404(subscription_id)
    return jsonify(subscription.serialize())

# CREATE a new subscription
@app.route('/subscriptions', methods=['POST'])
def create_subscription():
    """
    Add a new subscription.
    ---
    tags:
      - Subscription
    parameters:
      - name: subscription
        in: body
        type: object
        required: true
        schema:
          $ref: '#/definitions/NewSubscription'
    responses:
      201:
        description: Subscription created
        schema:
          $ref: '#/definitions/Subscription'
      400:
        description: Invalid subscription data
    """
    data = request.get_json()
    subscription = Subscription(title=data['title'],
                                description=data['description'],
                                language=data['language'],
                                pubDate=data['pubDate'],
                                user_id=data['user_id'],
                                subscribed_on=data['subscribed_on'],
                                image_url=data['image_url'],
                                url=data['url'],
                                author_name=data['author_name'])
    db.session.add(subscription)
    db.session.commit()
    return jsonify(subscription.serialize()), 200


# DELETE an existing subscription
@app.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    """
    Delete an existing subscription.
    ---
    tags:
      - Subscription
    parameters:
      - name: subscription_id
        in: path
        type: integer
        required: true
        description: ID of the subscription to delete
    responses:
      204:
        description: Subscription deleted
      404:
        description: Subscription not found
    """
    subscription = Subscription.query.get_or_404(subscription_id)
    db.session.delete(subscription)
    db.session.commit()


def get_app_db():
    return (app, db)


def run():
    app.run(debug=True)
