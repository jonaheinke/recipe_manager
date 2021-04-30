create table if not exists category (
	id integer primary key autoincrement,
	name text not null
);

create table if not exists recipe (
	id integer primary key autoincrement,
	name text not null,
	preptime integer,
	cooktime integer,
	baketime integer,
	cooltime integer,
	canbeprepareddaysearlier integer,
	img image
);



-- ingredients
create table if not exists ingredient (
	id integer primary key autoincrement,
	name text not null
);

create table if not exists r_recipe_ingredient (
	id integer foreign key references recipe(id),
	name text not null
);



-- steps
create table if not exists step (
	id integer primary key autoincrement,
	name text not null
);

create table if not exists r_recipe_steps (
	id integer primary key autoincrement,
	name text not null
);