import os
from dotenv         import load_dotenv
from sqlalchemy     import create_engine
from sqlalchemy     import text
from sqlalchemy.orm import Session


load_dotenv()

engine = create_engine(os.getenv('DATABASE_URI_dev'))

with Session(engine) as session:
  res = session.execute(text('select * from main'))
  for r in res:
    print(r)

