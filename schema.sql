DROP TABLE if EXISTS albums;
DROP TABLE if EXISTS pet;
DROP TABLE if EXISTS comments;
DROP TABLE if EXISTS colour;
DROP TABLE if EXISTS petColour;



CREATE TABLE pet (
        petId INTEGER PRIMARY KEY AUTOINCREMENT,
        reportType text,
        petType text,
        name text,
        reportDate date,
        postcodeArea text,
        postcodeIncode text,
        age text,
        sex text,
        description text,
        photo blob,
        ownerName text,
        ownerSurname text,
        email text
);

CREATE TABLE comments (
        commentId INTEGER PRIMARY KEY AUTOINCREMENT,
        name text,
        petId integer,
        commentDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        content text,
        FOREIGN KEY (petId)
                REFERENCES pet (petId)
);

CREATE TABLE colour (
        colourId INTEGER PRIMARY KEY AUTOINCREMENT,
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
