--Login_info contains information about the users name, password and role
--I don't think an extra table is neccessary for role (yet)
CREATE TABLE Login_info(
login_pk		serial primary key,
username		varchar(16),
password		varchar(16),
role			text
);

--Assets has a name, descriptin and current location(connected to a facility)
--There will be a facility called 'disposed' for now. extra table not needed
CREATE TABLE Assets(
asset_pk		serial primary key,
asset_tag		varchar(16),
description		text,
current_location	integer REFERENCES facilities (facility_pk)
);

--facilities contains a name and code. I don't think we need to know which
--assets are at a specific facility yet.  Tha will probably require an extra
--table or reworking of an existing one.  
CREATE TABLE facilities(
facility_pk		serial primary key,
facility_fk		varchar(32),
code			varchar(6)
);

