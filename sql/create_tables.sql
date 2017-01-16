CREATE TABLE products(
	product_pk serial primary key,
	vendor varchar(16) not null,
	description varchar(128) not null,
	alt_description varchar(128) not null
);

CREATE TABLE assets(
	asset_pk serial primary key,
	product_fk integer REFERENCES products(product_pk) not null,
	asset_tag varchar(16) not null,
	description varchar(16) not null,
	alt_description varchar(16) not null
);

CREATE TABLE vehicles(
	vehicle_pk serial primary key,
	asset_fk integer REFERENCES assets(asset_pk) not null
);

CREATE TABLE facilities(
	facility_pk serial primary key,
	fcode varchar(16) not null,
	common_name varchar(16) not null,
	location varchar(16) not null
);

CREATE TABLE asset_at(
	asset_fk integer REFERENCES assets(asset_pk) not null,
	facility_fk integer REFERENCES facilities(facility_pk) not null,
	arrive_dt timestamp,
	depart_dt timestamp
);

CREATE TABLE convoys(
	convoy_pk  serial primary key,
	request varchar(16),
	source_fk integer REFERENCES facilities(facility_pk) not null,
	dest_fk integer REFERENCES facilities(facility_pk) not null,
	depart_dt timestamp,
	arrive_dt timestamp
);

CREATE TABLE used_by(
	vehicle_fk integer REFERENCES vehicles(vehicle_pk) not null,
	convok_fk integer
);

CREATE TABLE asset_on(
	asset_fk integer  REFERENCES assets(asset_pk) not null,
	convoy_fk integer REFERENCES convoys(convoy_pk) not null,
	load_dt timestamp,
	unload_dt timestamp
);

CREATE TABLE users(
	user_pk  serial primary key,
	username varchar(128),
	active boolean
);

CREATE TABLE roles(
	role_pk serial primary key,
	title varchar(16)
);

CREATE TABLE user_is(
	user_fk integer REFERENCES users(user_pk) not null,
	role_fk integer REFERENCES roles(role_pk) not null
);

CREATE TABLE user_supports(
	user_fk integer REFERENCES users(user_pk) not null,
	facility_fk integer REFERENCES facilities(facility_pk) not null
);

CREATE TABLE levels(
	level_pk serial primary key,
	abbrv varchar(128),
	comment varchar(128)
);

CREATE TABLE compartments(
	compartment_pk serial primary key,
	abbrv varchar(128),
	comment varchar(128)
);

CREATE TABLE security_tags(
	tag_pk serial primary key,
	level_fk integer REFERENCES levels(level_pk) not null,
	compartment_fk integer REFERENCES compartments(compartment_pk) not null, 
	user_fk integer REFERENCES users(user_pk) not null,
	product_fk integer REFERENCES products(product_pk) not null,
	asset_fk integer REFERENCES assets(asset_pk) not null
);
