from sqlalchemy import create_engine, text, MetaData, Column, Table, Integer, String

db_engine = create_engine("sqlite:///:memory:", encoding = "utf-8", pool_size = 8)

meta = MetaData()
t = Table("name", meta,
	Column("id", Integer, primary_key = True),
	Column("content", String(40))
)

with db_engine.connect() as conn:
	with open("database_setup.sql") as f:
		conn.execute(text(f.read()))
	conn.commit()