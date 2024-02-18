import os
import json
import re
from typing import List

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy     import JSON

from . import docsTable
from . import ln_docs_tags
from . import db
from .tags import Tags
from src.mixins import MixinTimestamps
from schemas.serialization import SchemaSerializeDocJsonTimes


_prefix_by_doc_id = os.getenv('PREFIX_BY_DOC_ID')

_schemaDocsDump     = SchemaSerializeDocJsonTimes()
_schemaDocsDumpMany = SchemaSerializeDocJsonTimes(many = True)


# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes
class Docs(MixinTimestamps, db.Model):
  __tablename__ = docsTable

  id:   Mapped[int]  = mapped_column(primary_key = True)
  data: Mapped[dict] = mapped_column(JSON)

  # virtual
  tags: Mapped[List['Tags']] = relationship(secondary      = ln_docs_tags, 
                                            back_populates = 'docs')
  
  # magic
  def __repr__(self):
    return f'Docs({json.dumps(self.dump())})'

  @staticmethod
  def tagged(tag_name):
    tag = Tags.by_name(tag_name)
    return tag.docs if tag else []
  
  @staticmethod
  def dicts(docs, **kwargs):
    return _schemaDocsDumpMany.dump(docs, **kwargs)
  
  @staticmethod
  def by_tag_and_id(tag, id):
    doc = None

    try:
      doc = db.session.scalar(
        db.select(Docs)
          .join(Docs.tags)
          .where(Tags.tag == tag, Docs.id == id))
      
    except:
      pass
    
    return doc
  

  @staticmethod
  def var_by_name(var_name):
    doc = None
    for v in Docs.tagged('@vars'):
      if var_name in v.data:
        doc = v
        break
    return doc
  
  
  @staticmethod
  def by_doc_id(doc_id, *, create = False):
    # get single doc by id `doc_id: string` cached in 
    # `@tags.tag` collection, 
    #   ex. `kmPtHAgrysK://foo@56` 
    domain_ = f'{_prefix_by_doc_id}://{doc_id}@'
    tag_    = None
    doc     = None

    try:
      tag_ = db.session.scalar(
        db.select(Tags)
          .where(Tags.tag.like(f'{domain_}%')))
    
    except:
      pass
    
    else:
      if tag_:
        # doc found, resolve
        doc = db.session.get(Docs, re.match(r'.*@(\d+)$', tag_.tag).groups()[0])
      
      else:
        if True == create:
          
          # add default blank doc
          doc = Docs(data = {})          
          db.session.add(doc)
          db.session.commit()
          
          # add related tag
          tag_ = Tags(tag = f'{domain_}{doc.id}')
          db.session.add(tag_)
          db.session.commit()

    return doc
  
  
  def includes_tags(self, *args):
    tags_self = [t.tag for t in self.tags]
    return all(tag in tags_self for tag in args)
  
  def dump(self, **kwargs):
    return _schemaDocsDump.dump(self, **kwargs)
  
  