CREATE TABLE students_new (
    id INTEGER
    student_name TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE houses (
    id INTEGER,
    house TEXT,
    head TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE house_assignments (
    student_id INTEGER NOT NULL,
    house_id TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students_new(id)
);