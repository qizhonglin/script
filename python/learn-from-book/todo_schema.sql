create table project (
	name 		text primary key,
	description text,
	deadline 	date
);

create table task (
	id 				integer primary key autoincrement not null,
	priority 		integer default 1,
	details 		text,
	status 			text,
	deadline 		date,
	completed_on 	date,
	project			text not null references project(name)
);

insert into project (name, description, deadline) 
	values ('pymotw', 'Python MOdule of the Week', '2010-11-01');

insert into task (details, status, deadline, project)
	values('write about select', 'done', '2010-10-03', 'pymotw');
insert into task (details, status, deadline, project)
	values('write about random', 'waiting', '2010-10-10', 'pymotw');
insert into task (details, status, deadline, project)
	values('write about sqlite3', 'actie', '2010-10-17', 'pymotw');
