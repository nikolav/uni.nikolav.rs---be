import json
from pprint import pprint

from flask      import Blueprint
from flask      import request
from flask      import g
from flask_cors import CORS
from flask_cors import cross_origin
from flask      import make_response
from flask      import abort

from sqlalchemy import select
from sqlalchemy import literal_column
from sqlalchemy import text
from sqlalchemy import func

from flask_app       import db
from flask_app       import app
from models.tags     import Tags
from models.docs     import Docs
# from utils.pw       import hash  as hashPassword
# from utils.pw       import check as checkPassword
# from utils.jwtToken import issueToken
# from utils.jwtToken import setInvalid as tokenSetInvalid
# from config         import TAG_USERS

bp_testing = Blueprint('testing', __name__, url_prefix = '/test')

# cors blueprints as wel for cross-domain requests
cors_bp_testing = CORS(bp_testing)

from schemas.serialization   import SchemaSerializeDocJsonTimes as DocPlain
from marshmallow.exceptions  import ValidationError
from marshmallow  import Schema
from marshmallow  import fields
from marshmallow  import EXCLUDE

from middleware.arguments import arguments_schema

class SchemaTesting(Schema):

  class Meta:
    unknown = EXCLUDE
    
  x0 = fields.Integer(load_default = -1)

@bp_testing.route('/', methods = ('POST',))
@arguments_schema(SchemaTesting())
def testing_home():
  # Njvrw1gYEXd3yv:
  print('---')
  r = db.session.scalars(
    db.select(Tags).join(Tags.docs).where(
      # Docs.tags.any(Tags.tag == '@tasks:all'),
      Docs.id == 2845,
      # Tags.tag.like('Njvrw1gYEXd3yv:%'),
    )
  )
  print('---')
  print(r.all())
  return g.arguments, 200
