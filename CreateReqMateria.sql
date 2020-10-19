USE dac_database;
SET SQL_SAFE_UPDATES = 0;

DROP TABLE IF EXISTS requirements;
CREATE TABLE requirements(
    grupo INT not null,
    req varchar(20),
    idmateria varchar(20) not null,
    partial tinyint,
    year int,
    PRIMARY KEY (grupo, req, idmateria),
    CONSTRAINT fk_materia
    FOREIGN KEY (idmateria) 
        REFERENCES materia(idmateria)
	ON DELETE CASCADE
    ON UPDATE CASCADE
); 

DROP TABLE IF EXISTS semestres;
CREATE TABLE semestres(
    ind_semestre INT,
    materia varchar(20),
    idcurso varchar(20),
    PRIMARY KEY (idcurso, materia, ind_semestre),
    CONSTRAINT fk_curso
    FOREIGN KEY (idcurso) 
        REFERENCES curso(idcurso)
	ON DELETE CASCADE
    ON UPDATE CASCADE
);


