from models.tags import Tags
from config.graphql.init import query


@query.field('docsByTopic')
def resolve_docsByTopic(_obj, _info, topic):
  return [ doc.dump() for doc in Tags.by_name(topic, create = True).docs ]
