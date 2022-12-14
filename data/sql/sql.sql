DROP SCHEMA IF EXISTS projet CASCADE;
CREATE SCHEMA projet;

----------------
--CREATE TABLE--
----------------

CREATE TABLE projet.users (
    id_user SERIAL PRIMARY KEY,
    lastname varchar(100) NOT NULL check ( lastname<>'' ),
    firstname varchar(100) NOT NULL check ( firstname<>'' ),
    email VARCHAR(100) NOT NULL UNIQUE check ( email<>'' ),
    pseudo varchar(40) NOT NULL UNIQUE check ( pseudo<>'' ),
    sexe varchar(20) NOT NULL CHECK (sexe IN ('male', 'female', 'other')),
    phone varchar(40) check ( phone<>'' ),
    password char(60) NOT NULL
);

CREATE TABLE projet.chat_rooms  (
    id_room varchar(36) PRIMARY KEY,
    id_user1 INTEGER NOT NULL REFERENCES projet.users(id_user),
    id_user2 INTEGER NOT NULL REFERENCES projet.users(id_user)
);

CREATE TABLE projet.favorites (
    id_teacher INTEGER NOT NULL REFERENCES projet.users(id_user),
    id_student INTEGER NOT NULL REFERENCES projet.users(id_user),
    CONSTRAINT favorite_pk PRIMARY KEY (id_teacher, id_student)
);

CREATE TABLE projet.ratings (
    rating_text text NOT NULL check (rating_text<>''),
    rating_number INTEGER NOT NULL CHECK (rating_number IN (1,2,3,4,5)) ,
    id_rater INTEGER NOT NULL REFERENCES projet.users(id_user),
    id_rated INTEGER NOT NULL REFERENCES projet.users(id_user),
    CONSTRAINT rating_pk PRIMARY KEY (id_rater, id_rated),
    check ( id_rater<>ratings.id_rated )
);

CREATE TABLE projet.notifications (
    id_notification SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL REFERENCES projet.users(id_user),
    notification_text varchar(255) NOT NULL check ( notification_text<>'' ),
    notification_date TIMESTAMP NOT NULL DEFAULT NOW(),
    seen BOOLEAN NOT NULL DEFAULT false,
    chat_link varchar(100) DEFAULT ' '
);

CREATE TABLE projet.categories (
    id_category SERIAL PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE check ( name<>'' )
);

CREATE TABLE projet.teacher_skills (
    id_category INTEGER NOT NULL REFERENCES projet.categories(id_category),
    id_teacher INTEGER NOT NULL REFERENCES projet.users(id_user),
    CONSTRAINT teacher_skill_pk PRIMARY KEY (id_category, id_teacher)
);

CREATE TABLE projet.courses (
    id_course SERIAL PRIMARY KEY,
    id_category INTEGER NOT NULL REFERENCES projet.categories(id_category),
    id_teacher INTEGER NOT NULL REFERENCES projet.users(id_user),
    course_description text NOT NULL check ( course_description<>'' ),
    price_per_hour DOUBLE PRECISION NOT NULL,
    city varchar(70) NOT NULL check ( city<>'' ),
    country varchar(70) NOT NULL check ( country<>'' ),
    level varchar(30) NOT NULL check (level in ('Débutant', 'Intermédiaire', 'Confirmé'))
);

CREATE TABLE projet.appointments (
    id_course INTEGER NOT NULL REFERENCES projet.courses(id_course),
    id_student INTEGER NOT NULL REFERENCES projet.users(id_user),
    appointment_state varchar(20) CHECK (appointment_state IN ('pending','accepted', 'canceled', 'finished','not_come')) DEFAULT 'pending' NOT NULL check ( appointment_state<>'' ),
    appointment_date DATE NOT NULL,
    street varchar(100) NOT NULL check ( street<>'' ),
    number_house INTEGER NOT NULL,
    box_house varchar(10) check ( box_house<>'' ),
    CONSTRAINT appointment_pk PRIMARY KEY (id_course, id_student)
);

INSERT INTO projet.users (lastname, firstname, email, pseudo, sexe, phone,password)
VALUES ('Dupont', 'Pierre', 'requinFR@gmail.com', 'REQUIN', 'male', '(+32)4 77 123 659', '$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO'); -- password : password123

INSERT INTO projet.users (lastname, firstname, email, pseudo, sexe, phone,password)
VALUES ('Sarrabia', 'Pablo', 'espanaP@gmail.com', 'LaRoja', 'male', '(+32)4 87 123 721', '$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO'); -- password : password123

INSERT INTO projet.users (lastname, firstname, email, pseudo, sexe, phone,password)
VALUES ('Putellas', 'Alexia', 'barcelonaBO@gmail.com', 'Oro', 'female', '(+32)4 89 123 144', '$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO'); -- password : password123

INSERT INTO projet.users (lastname, firstname, email, pseudo, sexe, phone,password)
VALUES ('Patala', 'Morgane', 'morgane1780@gmail.com', 'morganeWemmel', 'female', '(+32)4 75 123 449', '$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO'); -- password : password123

INSERT INTO projet.users (lastname, firstname, email, pseudo, sexe, phone,password)
VALUES ('Soler', 'Carlos', 'PSGfan@gmail.com', 'soleil', 'male', '(+32)4 77 321 559', '$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO'); -- password : password123

INSERT INTO projet.categories (name)
VALUES ('Anglais');

INSERT INTO projet.categories (name)
VALUES ('Arabe');

INSERT INTO projet.categories (name)
VALUES ('Dessin');

INSERT INTO projet.categories (name)
VALUES ('Espagnol');

INSERT INTO projet.categories (name)
VALUES ('Finance');

INSERT INTO projet.categories (name)
VALUES ('Java');

INSERT INTO projet.categories (name)
VALUES ('Math');

INSERT INTO projet.categories (name)
VALUES ('Musique');

INSERT INTO projet.categories (name)
VALUES ('PHP');

INSERT INTO projet.categories (name)
VALUES ('Physique');

INSERT INTO projet.categories (name)
VALUES ('Piano');

INSERT INTO projet.categories (name)
VALUES ('Python');

INSERT INTO projet.teacher_skills(id_category, id_teacher)
VALUES (1, 1);

INSERT INTO projet.teacher_skills(id_category, id_teacher)
VALUES (2, 1);

INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (9,1,'Cours permettant de vous introduire le langage PHP. Aucun prérequis n''est nécessaire', 18, 'Bruxelles', 'Belgique','Débutant');

INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (7,1,'Cours particulier sur les fonctions du second degré', 25, 'Bruxelles', 'Belgique','Intermédiaire');

INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (1,1,'Cours d Anglais avec Browny', 25, 'Bruxelles', 'Belgique','Débutant');

INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (9,1,'Cours d e PHP', 25, 'Bruxelles', 'Belgique','Débutant');

INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (12,1,'Cours de Python', 25, 'Bruxelles', 'Belgique','Débutant');

INSERT INTO projet.appointments(id_course, id_student, appointment_state, appointment_date, street, number_house)
VALUES(1, 5, 'pending', '2022-10-20', 'rue de la colline', 121);

INSERT INTO projet.appointments(id_course, id_student, appointment_state, appointment_date, street, number_house)
VALUES(1, 1, 'accepted', '2022-10-20', 'rue de la colline', 121);

INSERT INTO projet.appointments(id_course, id_student, appointment_state, appointment_date, street, number_house)
VALUES(2, 1, 'canceled', '2022-10-20', 'rue de la colline', 121);

INSERT INTO projet.appointments(id_course, id_student, appointment_state, appointment_date, street, number_house)
VALUES(3, 2, 'finished', '2022-10-20', 'rue de la colline', 121);

INSERT INTO projet.appointments(id_course, id_student, appointment_state, appointment_date, street, number_house)
VALUES(4, 1, 'finished', '2022-10-20', 'rue de la colline', 121);

INSERT INTO projet.appointments(id_course, id_student, appointment_state, appointment_date, street, number_house)
VALUES(5, 1, 'not_come', '2022-10-20', 'rue de la colline', 121);

INSERT INTO projet.ratings(rating_text, rating_number, id_rater, id_rated)
VALUES('Prof qui explique très bien, je recommande', 5, 5, 1);

INSERT INTO projet.notifications(id_user, notification_text, notification_date, seen)
VALUES (1, 'Une nouvelle notif pour toi bebou', now(), FALSE);

INSERT INTO projet.notifications(id_user, notification_text, notification_date, seen)
VALUES (1, 'Une nouvelle notif pour toi bebou', now(), FALSE);
