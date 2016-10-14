DROP TABLE IF EXISTS card;
CREATE TABLE card
(
	cardid int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name varchar(255) NOT NULL,
	category enum('Medication', 'Nutrition', 'Disease') NOT NULL,
	wiki_title varchar(255) NOT NULL
) ;
DESCRIBE card;

DROP TABLE IF EXISTS coach_plan_package;
CREATE TABLE coach_plan_package
(
	packageid int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name varchar(255) NOT NULL,
	description varchar(1024),
	diagnosis varchar(255)
);
DESCRIBE coach_plan_package;

DROP TABLE IF EXISTS coach_plan;
CREATE TABLE coach_plan
(
	planid int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
	packageid int unsigned,
	start_day int unsigned NOT NULL,
	end_day int unsigned NOT NULL,
	cardid int unsigned,
	FOREIGN KEY (packageid) REFERENCES coach_plan_package(packageid),
 	FOREIGN KEY (cardid) REFERENCES card(cardid)
);
DESCRIBE coach_plan;
