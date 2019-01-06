import sqlalchemy as sa
from datetime import datetime

metadata = sa.MetaData()

messages_pg = sa.Table('messages', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('message', sa.String(255)),
    sa.Column('date', sa.Date, default=datetime.utcnow()))
