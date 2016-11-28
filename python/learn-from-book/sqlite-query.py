import sqlite3

db_filename = 'todo.db'

with sqlite3.connect(db_filename) as conn:
	conn.row_factory = sqlite3.Row

	cursor = conn.cursor()
	query = """
		select id, priority, details, status, deadline 
		from task	
		where project = :project_name
		order by deadline
 	"""
	cursor.execute(query, {'project_name': 'pymotw'})

	for row in cursor.fetchall():
		print '%2d {%d} %-25s [%-8s] (%s)' % (row['id'], row['priority'], row['details'], row['status'], row['deadline'])

