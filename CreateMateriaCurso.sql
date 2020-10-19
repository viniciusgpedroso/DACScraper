USE dac_database;
SET SQL_SAFE_UPDATES = 0;

DROP TABLE IF EXISTS materia;
CREATE TABLE materia(
    idmateria varchar(20) not null,
    year int,
    title varchar(150),
    codes varchar(200),
    syllabus varchar(10000),
    PRIMARY KEY (idmateria)
);

DROP TABLE IF EXISTS curso;
CREATE TABLE curso(
    idcurso varchar(20) not null,
    code int,
    year int,
    emphasis varchar(20),
    name varchar(100),
    text_electives varchar(10000),
    PRIMARY KEY (idcurso)
);
