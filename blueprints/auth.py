from flask      import Blueprint
from flask      import g
from flask_cors import CORS

from flask_app      import db
from models.tags    import Tags
from models.docs    import Docs
from utils.pw       import hash  as hashPassword
from utils.pw       import check as checkPassword
from utils.jwtToken import issueToken
from utils.jwtToken import setInvalid as tokenSetInvalid
from config         import TAG_USERS

from middleware.arguments    import arguments_schema
from schemas.validation.auth import SchemaAuthLogin
from schemas.validation.auth import SchemaAuthRegister


# router config
bp_auth = Blueprint('auth', __name__, url_prefix = '/auth')

# cors blueprints as wel for cross-domain requests
cors_bp_auth = CORS(bp_auth)

@bp_auth.route('/register', methods = ('POST',))
@arguments_schema(SchemaAuthRegister())
def auth_register():
  email    = g.arguments['email']
  password = g.arguments['password']
  
  token = ''
  error = '@error/internal.500'

  try:
    tag = Tags.by_name(TAG_USERS)

    # skip if already registered
    if any(email == doc.data['email'] for doc in tag.docs):
      raise Exception('access denied')
    
    # register
    dataNewUser = { 
      'email'    : email, 
      'password' : hashPassword(password)
    }
    docNewUser = Docs(data = dataNewUser)
    tag.docs.append(docNewUser)
    db.session.commit()

    # new user added, get access-token
    token = issueToken({ 'id': docNewUser.id })
    
  except Exception as err:
    error = err
  
  else:
    # user registered, send token, 201
    if token:
      return { 'token': token }, 201
  
  # forbiden otherwise
  return { 'error': str(error) }, 403
  
  
@bp_auth.route('/login', methods = ('POST',))
@arguments_schema(SchemaAuthLogin())
def auth_login():
  email    = g.arguments['email']
  password = g.arguments['password']
  
  docUser = None
  token   = ''
  error   = '@error/internal.500'
  
  
  try:
    for doc in Docs.tagged(TAG_USERS):
      if email == doc.data['email']:
        if not checkPassword(password, doc.data['password']):
          raise Exception('access denied')
        docUser = doc
        break

    if docUser:
      token = issueToken({ 'id': docUser.id })
      
  except Exception as err:
    error = err

  else:
    if token:
      return { 'token': token }, 200

  return { 'error': str(error) }, 401


@bp_auth.route('/logout', methods = ('POST',))
def auth_logout():
  error = '@error/internal.500'
  try:
    tokenSetInvalid(g.access_token)
  except Exception as err:
    error = err
  else:
    return {}, 200
  
  return { 'error': str(error) }, 500
  
@bp_auth.route('/who', methods = ('GET',))
def auth_who():
  error = '@error/internal.500'
  try:
    # send user data
    return { 'id': g.user.id, 'email': g.user.data['email'] }, 200
  except Exception as err:
    error = err
  
  return { 'error': str(error) }, 500
