import os

from flask_app import db


tblSuffix       = os.getenv('TABLE_NAME_SUFFIX')
lnTableDocsTags = f'ln_docs_tags{tblSuffix}'
docsTable       = f'docs{tblSuffix}'
tagsTable       = f'tags{tblSuffix}'

ln_docs_tags = db.Table(
  lnTableDocsTags,
  db.Column('doc_id', db.ForeignKey(f'{docsTable}.id'), primary_key = True),
  db.Column('tag_id', db.ForeignKey(f'{tagsTable}.id'), primary_key = True),
)
