import sqlalchemy as sa

metadata = sa.MetaData()

messages = sa.Table('messages', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('message', sa.String(255)))

