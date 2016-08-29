import os
import sqlite3

db_filename = 'todo.db'
schema_filename = 'todo_schema.sql'

db_is_new = not os.path.exists(db_filename)
with sqlite3.connect(db_filename) as conn:
	if db_is_new:
		print 'Creating schema'
		with open(schema_filename, 'rt') as f:
			schema = f.read()
		conn.executescript(schema)
	else:
		print 'Database exists'
	
