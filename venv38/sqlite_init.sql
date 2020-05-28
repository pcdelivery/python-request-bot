create table requests_questions(
    title varchar(255) primary key,
    size integer
);

create table requests_answers(
    text varchar(255) primary key,
    is_true boolean
);