CREATE TABLE Persons (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    patronymic VARCHAR(100),
    face_encoding BYTEA NOT NULL,
    photo BYTEA NOT NULL
);

CREATE TABLE Sightings (
    id SERIAL PRIMARY KEY,
    person_id INT NOT NULL,
    sighting_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    camera_photo BYTEA NOT NULL,
    FOREIGN KEY (person_id) REFERENCES Persons(id)
);