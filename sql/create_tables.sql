CREATE TABLE roles (
    role_pk serial primary key, /* numeric primary key to keep track of users*/
    title   varchar(128)        /* title of the role */
);

CREATE TABLE users (
    user_pk  serial primary key,               /* numeric primary key to keep track of each user */
    role_fk  int REFERENCES roles (role_pk),   /*references role_pk in roles*/
    username varchar(16),                      /* max 16 characters long  */
    password varchar(16)                       /* max 16 characters long  */
);

CREATE TABLE assets(
    asset_pk     serial primary key, /*numeric primary key to keep track of assets*/
    tag          varchar(16),        /*an asset tag upto 16 characters in length*/
    description  varchar(128),
    disposed     boolean default false,
    in_transit   boolean default false
);

CREATE TABLE facilities(
    facility_pk   serial primary key, /*numeric primary key to keep track of facilities*/ 
    common_name   varchar(32),        /*name of the facility up to 32 charaters*/
    facility_code varchar(8)          /*facility code up to eight characters*/
);

CREATE TABLE asset_location(
    asset_fk    int REFERENCES assets (asset_pk) default null,        /*references asset_pk in assets*/
    facility_fk int REFERENCES facilities (facility_pk) default null, /*references facility_pk in facilities*/
    arrive      date default null,                                    /*date arived*/
    depart      date default null                                     /*date departed*/
);
