-- Database: StationZuil

-- DROP DATABASE IF EXISTS "StationZuil";

CREATE DATABASE "StationZuil"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

create table Beoordeling (
	beoordelingnr serial not null,
	is_goedgekeurd bool,
	datum date,
	tijd time,
	moderator_email varchar(320) not null,
	primary key (beoordelingnr)
);

create table Bericht (
	berichtnr serial not null,
	tekst varchar(140),
	datum date,
	tijd time,
	naam varchar(20),
	station varchar(20),
	Beoordelingnr int not null,
	primary key (berichtnr)
);

create table Moderator (
	email varchar(320) not null,
	naam varchar(20),
	wachtwoord varchar(30),
	primary key (email)
);

alter table Bericht
add constraint FKBericht
foreign key (Beoordelingnr)
references Beoordeling (beoordelingnr);

alter table Beoordeling
add constraint FKBeoordeling
foreign key (Moderator_email)
references Moderator (email);
