from flask import request, jsonify
from app.models.lead_model import Lead
from app.configs.database import db
from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound



def create_lead():
    data = request.get_json()

    if not Lead.check_json_types(data):
        return {'error': 'Todos os campos passados devem ser uma string'}, 400

    data = Lead.add_dates(data)

    try:
        lead = Lead(**data)

        session: Session = db.session()
        session.add(lead)
        session.commit()

    except IntegrityError:
        return {"error": "email e telefone devem ser unicos."}, 409

    return jsonify(lead), 201


def retrieve_leads():
    session : Session = db.session
    base_query: Query = session.query(Lead)

    leads = base_query.order_by(Lead.visits.desc()).all()

    if not leads:
        return {"msg": "nenhuma lead cadastrada"}, 200

    return jsonify(leads), 200


def add_visit():
    data = request.get_json()

    try:
        if not len(data.keys()) == 1:
            return {"error": "passe somente o email como chave"}, 400

        email = data['email']
    except KeyError:
        return {"error": "passe somente o email como chave"}, 400
    
    if type(email) != str:
        return {"error": "passe o email como string"}, 400


    session: Session = db.session

    base_query: Query = db.session.query(Lead)
    email_query: BaseQuery = base_query.filter_by(email=email)

    try:
        lead = email_query.first_or_404(description='email nao cadastrado')
    except NotFound as e:
        return {"error": e.description}, 404

    lead = lead.patch_visits()

    session.commit()

    return "", 204


def delete_lead():
    data = request.get_json()

    try:
        if not len(data.keys()) == 1:
            return {"error": "passe somente o email como chave"}, 400

        email = data['email']
    except KeyError:
        return {"error": "passe somente o email como chave"}, 400
    
    if type(email) != str:
        return {"error": "passe o email como string"}, 400

    session: Session = db.session

    base_query: Query = db.session.query(Lead)
    email_query: BaseQuery = base_query.filter_by(email=email)

    try:
        lead = email_query.first_or_404(description='email nao cadastrado')
    except NotFound as e:
        return {"error": e.description}, 404
    
    session.delete(lead)

    session.commit()

    return "", 204
