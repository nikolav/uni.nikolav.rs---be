PATHS_SKIP_AUTH = (
  
  # status check
  r'^/$',
  
  # auth 
  r'^/auth/register$',
  r'^/auth/login$',
  
  r'^/storage/[0-9a-fA-F]+$',
)

TAG_USERS        = '@users'
TAG_VARS         = '@vars'
TAG_TOKEN_VALID  = '@token/valid'
TAG_IS_FILE      = '@isfile'
TAG_STORAGE      = '@storage:'


init_docs_tags = (TAG_USERS, TAG_VARS, TAG_TOKEN_VALID, TAG_IS_FILE)


KEY_TOKEN_CREATED_AT = '@'
