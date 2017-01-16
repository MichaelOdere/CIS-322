CREATE TABLE products(
	product_pk integer,
	vendor varchar(128) not null,
	description varchar(128) not null,
	alt_description varchar(128) not null
);

CREATE TABLE assets(
	asset_pk integer,
	product_fk integer,
	asset_tag varchar(128) not null,
	description varchar(128) not null,
	alt_description varchar(128) not null
);

CREATE TABLE vehicles(
	vehicle_pk integer,
	asset_fk integer
);

CREATE TABLE facilities(
	facility_pk integer,
	fcode varchar(128) not null,
	common_name varchar(128) not null,
	location varchar(128) not null
);

CREATE TABLE asset_at(
	asset_fk integer,
	facility_fk integer,
	arrive_dt timestamp,
	depart_dt timestamp
);

CREATE TABLE convoys(
	convoy_py integer,
	request varchar(128),
	source_fk integer,
	dest_fk integer,
	depart_dt timestamp,
	arrive_dt timestamp
);

CREATE TABLE used_by(
	vehicle_fk integer,
	convok_fk integer
);

CREATE TABLE asset_on(
	asset_fk integer,
	convoy_fk integer,
	load_dt timestamp,
	unload_dt timestamp
);

CREATE TABLE users(
	user_pk integer,
	username varchar(128),
	active boolean
);

CREATE TABLE roles(
	role_pk integer,
	title varchar(128)
);

CREATE TABLE user_is(
	user_fk integer,
	role_fk integer
);

CREATE TABLE user_supports(
	user_fk integer,
	facility_fk integer
);

CREATE TABLE levels(
	level_pk integer,
	abbrv varchar(128),
	comment varchar(128)
);

CREATE TABLE compartments(
	compartment_pk integer,
	abbrv varchar(128),
	comment varchar(128)
);

CREATE TABLE security_tags(
	tag_pk integer,
	level_fk integer,
	compatment_fk integer,
	user_fk integer,
	product_fk integer,
	asset_fk integer
);
