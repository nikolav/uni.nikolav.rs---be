import os

from flask_app   import db
from models.tags import Tags
from models.docs import Docs
from .           import init_docs_tags
from config      import TAG_VARS
from config      import TAG_USERS
from utils.pw    import hash as hashPassword


for t in init_docs_tags:
  Tags.by_name(t, create = True)

tag_vars = Tags.by_name(TAG_VARS)

vars_data = [doc.data for doc in tag_vars.docs]

if all(not 'app:name' in node for node in vars_data):
  tag_vars.docs.append(Docs(data = { 'app:name': "app:nuxtflask" }))

if all(not 'admin:email' in node for node in vars_data):
  tag_vars.docs.append(Docs(data = { 'admin:email': "admin@nikolav.rs" }))
  
db.session.commit()


email_    = os.getenv('ADMIN_EMAIL')
password_ = os.getenv('ADMIN_PASSWORD')

docAdmin  = None
tag_users = Tags.by_name(TAG_USERS);

for d in tag_users.docs:
  if email_ == d.data['email']:
    docAdmin = d
    break

if not docAdmin:
  docAdmin = Docs(data = { 
                'email'    : email_, 
                'password' : hashPassword(password_) 
              })
  tag_users.docs.append(docAdmin)
  db.session.add(docAdmin)

db.session.commit()


policy_admins_ = os.getenv('POLICY_ADMINS')
policy_email_  = os.getenv('POLICY_EMAIL')
policy_fs_     = os.getenv('POLICY_FILESTORAGE')
policy_all_    = os.getenv('POLICY_ALL')

tagPolicyADMINS = Tags.by_name(policy_admins_, create = True)
tagPolicyEMAIL  = Tags.by_name(policy_email_,  create = True)
tagPolicyFS     = Tags.by_name(policy_fs_,     create = True)
tagPolicyALL    = Tags.by_name(policy_all_,    create = True)

if not docAdmin.includes_tags(policy_admins_):
  tagPolicyADMINS.docs.append(docAdmin)
if not docAdmin.includes_tags(policy_email_):
  tagPolicyEMAIL.docs.append(docAdmin)
if not docAdmin.includes_tags(policy_fs_):
  tagPolicyFS.docs.append(docAdmin)
# if not docAdmin.includes_tags(policy_all_):
#   tagPolicyALL.docs.append(docAdmin)

db.session.commit()
