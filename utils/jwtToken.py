import os
import re
from datetime import datetime

import jwt
from flask import request

from flask_app   import db
from models.tags import Tags
from models.docs import Docs
from config      import KEY_TOKEN_CREATED_AT
from config      import TAG_TOKEN_VALID


def __with_created_at(payload):
  payload[KEY_TOKEN_CREATED_AT] = str(datetime.utcnow())
  return payload


def tokenFromRequest():
  return re.match(r'^Bearer (.+)$', request.headers.get('Authorization')).groups()[0]


def decode(sToken):
  return jwt.decode(sToken, os.getenv('JWT_SECRET_ACCESS_TOKEN'), algorithms = ('HS256',))


def expired(token):
  jsonTokenPayload = token if isinstance(token, dict) else decode(token)
  ddif = datetime.utcnow() - datetime.fromisoformat(jsonTokenPayload[KEY_TOKEN_CREATED_AT])
  return int(os.getenv('JWT_EXPIRE_SECONDS')) < ddif.total_seconds()
  

def encode(jsonPayload):
  return jwt.encode(__with_created_at(jsonPayload),
    os.getenv('JWT_SECRET_ACCESS_TOKEN'),
    algorithm = 'HS256'
  )
  

def issueToken(jsonPayload):
  # generate token
  # store under '@token/valid' tag
  
  token = encode(jsonPayload)
  tag   = Tags.by_name(TAG_TOKEN_VALID)

  # add valid tokens '@token/valid' list
    
  docTokenValid = Docs(data = { f'{token}': 1 })
  tag.docs.append(docTokenValid)
  
  db.session.commit()

  return token
  

def valid(token):
  tag = Tags.by_name(TAG_TOKEN_VALID)
  return any(token in doc.data for doc in tag.docs) if tag else False


def setInvalid(token):
  if token:
    for doc in Docs.tagged(TAG_TOKEN_VALID):
      if token in doc.data:
        db.session.delete(doc)
        db.session.commit()
        break


def clearExpiredAll():
  for doc in Docs.tagged(TAG_TOKEN_VALID):
    for token in doc.data:
      if expired(token):
        db.session.delete(doc)
  db.session.commit()
