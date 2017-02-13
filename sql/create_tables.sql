CREATE TABLE users (
    user_pk serial primary key, /* numeric primary key to keep track of each user */
    username varchar(16), /* max 16 characters long  */
    password varchar(16)  /* max 16 characters long  */
);
