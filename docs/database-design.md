# Database design

![Database diagram](database-diagram.svg)

Database diagram for the project.

## CREATE TABLE statements
```
CREATE TABLE accounts (
	id INTEGER NOT NULL, 
	username TEXT NOT NULL, 
	password_hash TEXT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);

CREATE TABLE ingredients (
	id INTEGER NOT NULL, 
	name TEXT NOT NULL, 
	account_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES accounts (id)
);

CREATE TABLE recipe_ingredient (
	id INTEGER NOT NULL, 
	amount NUMERIC NOT NULL, 
	amount_unit TEXT NOT NULL, 
	ingredient_id INTEGER NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ingredient_id) REFERENCES ingredients (id), 
	FOREIGN KEY(recipe_id) REFERENCES recipes (id)
);

CREATE TABLE recipes (
	id INTEGER NOT NULL, 
	name TEXT NOT NULL, 
	description TEXT NOT NULL, 
	steps TEXT NOT NULL, 
	account_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES accounts (id)
);

CREATE TABLE shopping_list_items (
	id INTEGER NOT NULL, 
	amount NUMERIC NOT NULL, 
	amount_unit TEXT NOT NULL, 
	ingredient_id INTEGER NOT NULL, 
	account_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ingredient_id) REFERENCES ingredients (id), 
	FOREIGN KEY(account_id) REFERENCES accounts (id)
);
```
