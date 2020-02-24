# Database design

## Normalization
The database was first normalized to fourth normal form and then the following
denormalizations were performed:
- Table `accounts`
  - Column `username` could be used as the primary key since values in the
    column are unique. A separate `id` column is used instead to enable updating
    `username` without invalidating foreign key references to the updated row.

## Design notes
Association tables `shopping_list_items` and `recipe_ingredient` contain
ingredient amount information in addition to foreign key columns. This
simplifies the structure of the database and eases implementation compared to
having a separate table for amount information.

In table `shopping_list_items` a seperate `id` column is used as the primary
key instead of a composite primary key on columns `ingredient_id` and
`account_id`. This allows a user to store multiple entries for the same
ingredient using different amounts and units. A composite primary key consisting
of all the columns in the table could be used as the primary key, but that would
unnecessarily increase the size of the primary key index. The same reasoning
applies to the table `recipe_ingredient`.

Table `ingredients` has a foreign key column `account_id` referencing the
`accounts` table. This relationship can be derived using other tables, namely
`ingredients ⟶ shopping_list_items ⟶ accounts` and `ingredients ⟶
recipe_ingredient ⟶ recipes ⟶ accounts`. A separate column improves the
performance of some SQL queries used in the application, especially a query used
to fetch ingredient completions for an ingredient name. The query is executed
every time the user edits the name, and therefore the query has to be
performant.

## Database diagram
![Database diagram](database-diagram.svg)

## Schema
```sql
CREATE TABLE accounts (
	id INTEGER NOT NULL,
	username TEXT NOT NULL,
	password_hash TEXT NOT NULL,
	role TEXT NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (username)
);
CREATE TABLE ingredients (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	account_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(account_id) REFERENCES accounts (id) ON DELETE CASCADE
);
CREATE INDEX idx_ingredient_account_id_name_lower ON ingredients (account_id, lower(name));
CREATE TABLE recipes (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXT NOT NULL,
	steps TEXT NOT NULL,
	account_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(account_id) REFERENCES accounts (id) ON DELETE CASCADE
);
CREATE INDEX ix_recipes_account_id ON recipes (account_id);
CREATE TABLE recipe_ingredient (
	id INTEGER NOT NULL,
	amount NUMERIC NOT NULL,
	amount_unit TEXT NOT NULL,
	ingredient_id INTEGER NOT NULL,
	recipe_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(ingredient_id) REFERENCES ingredients (id) ON DELETE CASCADE,
	FOREIGN KEY(recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
);
CREATE INDEX ix_recipe_ingredient_recipe_id ON recipe_ingredient (recipe_id);
CREATE INDEX ix_recipe_ingredient_ingredient_id ON recipe_ingredient (ingredient_id);
CREATE TABLE shopping_list_items (
	id INTEGER NOT NULL,
	amount NUMERIC NOT NULL,
	amount_unit TEXT NOT NULL,
	ingredient_id INTEGER NOT NULL,
	account_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(ingredient_id) REFERENCES ingredients (id) ON DELETE CASCADE,
	FOREIGN KEY(account_id) REFERENCES accounts (id) ON DELETE CASCADE
);
CREATE INDEX ix_shopping_list_items_account_id ON shopping_list_items (account_id);
CREATE INDEX ix_shopping_list_items_ingredient_id ON shopping_list_items (ingredient_id);

```
