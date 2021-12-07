DROP TABLE if EXISTS albums;

CREATE TABLE pet (
	petId integer PRIMARY KEY,
	reportType text,
	petType text,
	name text,
	reportDate date,
	postcodeArea text,
	postcodeIncode text,
	age text,
	sex text,
	desription text,
	photo blob,
	ownerName text,
	ownerSurname text,
	email text
);	

CREATE TABLE comments (
	commentId integer PRIMARY KEY,
	name text,
	petId integer,
	commentDate date,
	content text,
	FOREIGN KEY (petId)
		REFERENCES pet (petId)
);

CREATE TABLE colour (
	colourId integer PRIMARY KEY,
	category text,
	name text
);

CREATE TABLE petColour (
	petId integer,
	colourId integer,
	PRIMARY KEY(petId,colourId),
	FOREIGN KEY (petId)
		REFERENCES pet (petId),
	FOREIGN KEY (colourId) 
		REFERENCES colour (colourId)
);	
