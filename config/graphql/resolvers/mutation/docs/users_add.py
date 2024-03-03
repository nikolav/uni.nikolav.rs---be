
from flask_app import db
from flask_app import io

from models.docs import Docs
from models.tags import Tags

from config import TAG_USERS
from config.graphql.init import mutation

from utils.pw import hash as hashPassword
from . import IOEVENT_JsonData


@mutation.field('docsUsersAdd')
def resolve_docsUsersAdd(_obj, _info, email, password):
  ID = None
  
  try:
    tag_users = Tags.by_name(TAG_USERS)
    
    if any(email == doc.data['email'] for doc in tag_users.docs):
      raise Exception('--user exists--')
    
    # user.add
    data_new_user = {
      'email'    : email,
      'password' : hashPassword(password)
    }
    doc_new_user = Docs(data = data_new_user)
    tag_users.docs.append(doc_new_user)
    db.session.commit()

    ID = doc_new_user.id
    
  except:
    pass
  
  else:
    if None != ID:
      io.emit(f'{IOEVENT_JsonData}{TAG_USERS}')          
  
  return ID
