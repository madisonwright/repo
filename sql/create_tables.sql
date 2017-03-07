--Login_info contains information about the users name, password and role
--I don't think an extra table is neccessary for role (yet)
CREATE TABLE Login_info(
login_pk		serial primary key,
username		varchar(16),
password		varchar(16),
role			text,
Active			boolean DEFAULT true
);

--facilities contains a name and code. I don't think we need to know which
--assets are at a specific facility yet.  Tha will probably require an extra
--table or reworking of an existing one.  
CREATE TABLE facilities(
facility_pk		serial primary key,
facility_fk		varchar(32),
code			varchar(6)
);

--Assets has a name, descriptin and current location(connected to a facility)
--There will be a facility called 'disposed' for now and a date for it.  
--extra table not needed yet
CREATE TABLE Assets(
asset_pk		serial primary key,
asset_tag		varchar(16),
description		text,
current_location	integer REFERENCES facilities (facility_pk),
arrived			text,
disposal_date		text
);

---Creates a request table with information aout the request
Create TABLE request(
request_pk		serial primary key,
log_officer		integer REFERENCES Login_info (login_pk),
fac_officer		integer REFERENCES Login_info (login_pk),
submit_date		text,
submit_time		text,
approved_date		text,
approved_time		text,
load_time		text,
unload_time		text,
destination		integer REFERENCES facilities (facility_pk),
asset			integer REFERENCES Assets (asset_pk),
approved		boolean
);


--- History table that holds all asset transactions.  Not currently implemented since
--- I did not opt for the extra credit step 7
Create TABLE History(
asset			integer REFERENCES Assets (asset_pk),
current_location	integer REFERENCES facilities (facility_pk),
load_time		text,
destination		integer REFERENCES facilities (facility_pk),
unload_time		text
);

