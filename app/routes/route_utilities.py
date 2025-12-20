from flask import abort, make_response
from ..db import db

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    model = db.session.get(cls, model_id)

    if not model:
        response = {"details": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model