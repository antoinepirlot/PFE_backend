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
    chat_link VARCHAR(100) DEFAULT ' '

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




------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------INSERTS-----------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------



-- USERS
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



-- CATEGORIES
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



-- TEACHER_SKILLS
INSERT INTO projet.teacher_skills(id_category, id_teacher)
VALUES (9, 1);

INSERT INTO projet.teacher_skills(id_category, id_teacher)
VALUES (9, 3);

INSERT INTO projet.teacher_skills(id_category, id_teacher)
VALUES (7, 2);

INSERT INTO projet.teacher_skills(id_category, id_teacher)
VALUES (12, 1);

INSERT INTO projet.teacher_skills(id_category, id_teacher)
VALUES (1, 4);


-- COURSES
INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (9,1,'Cours permettant de vous introduire le langage PHP. Aucun prérequis n''est nécessaire', 18, 'Bruxelles', 'Belgique','Débutant');

INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (7,2,'Cours particulier sur les fonctions du second degré', 22, 'Paris', 'France','Intermédiaire');

INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (1,4,'Cours d Anglais de niveau B1', 32, 'Namur', 'Belgique', 'Confirmé');

INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (9,3,'Un cours de PHP vous apprenant comment écrire vos propres fonctions personnelles et vos procédures', 25, 'Bruxelles', 'Belgique','Débutant');

INSERT INTO projet.courses(id_category, id_teacher, course_description, price_per_hour, city, country, level)
VALUES (12,1,'Apprendre les bases du Python, ', 25, 'Bruxelles', 'Belgique','Débutant');



-- FAVORITES
INSERT INTO projet.favorites(id_teacher, id_student)
VALUES (1, 3);

INSERT INTO projet.favorites(id_teacher, id_student)
VALUES (4, 2);


-- RATINGS
INSERT INTO projet.ratings(rating_text, rating_number, id_rater, id_rated)
VALUES('Prof qui explique très bien, je recommande', 5, 5, 1);

INSERT INTO projet.ratings(rating_text, rating_number, id_rater, id_rated)
VALUES('Prend le temps de bien expliquer les différents concepts même si parfois un peu trop flou, merci :)', 4, 3, 2);



-- NOTIFICATIONS


-- CHAT_ROOMS

