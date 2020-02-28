# User stories

SQL queries are copied from application logs when testing the application on an
SQLite database.

## Accounts
*As a user, I want to register to the app.*
```sql
-- Check for duplicate usernames.
SELECT EXISTS (SELECT *
FROM accounts
WHERE accounts.username = ?) AS anon_1

-- Insert new account row.
INSERT INTO accounts (username, password_hash, role) VALUES (?, ?, ?)
```
*As a user, I want to see statistics about my account*
```sql
-- Shopping list item count for current user.
SELECT count(*) AS count_1
FROM (SELECT shopping_list_items.id AS shopping_list_items_id, shopping_list_items.amount AS shopping_list_items_amount, shopping_list_items.amount_unit AS shopping_list_items_amount_unit, shopping_list_items.ingredient_id AS shopping_list_items_ingredient_id, shopping_list_items.account_id AS shopping_list_items_account_id
FROM shopping_list_items
WHERE shopping_list_items.account_id = ?) AS anon_1

-- Recipe count for current user.
SELECT count(*) AS count_1
FROM (SELECT recipes.id AS recipes_id, recipes.name AS recipes_name, recipes.description AS recipes_description, recipes.steps AS recipes_steps, recipes.account_id AS recipes_account_id
FROM recipes
WHERE recipes.account_id = ?) AS anon_1

-- Usernames and recipe counts for top recipe collecting users.
SELECT accounts.username username, COUNT(recipes.id) recipe_count
FROM accounts
LEFT JOIN recipes ON recipes.account_id = accounts.id
GROUP BY accounts.username
ORDER BY COUNT(recipes.id) DESC, accounts.username
LIMIT ?
```
*As a user, I want to be able to change my password.*
```sql
-- Update password for account row.
UPDATE accounts SET password_hash=? WHERE accounts.id = ?
```
*As a user, I want to be able to delete my account.*
```sql
-- Delete account row for current account id.
DELETE FROM accounts WHERE accounts.id = ?
```

## Recipes
*As a user, I want to add recipes to the recipe book.*
```sql
-- Insert row for recipe.
INSERT INTO recipes (name, description, steps, account_id) VALUES (?, ?, ?, ?)

-- Check if the ingredient exists. This query is executed for all ingredients
-- in the recipe.
SELECT ingredients.id AS ingredients_id, ingredients.name AS ingredients_name, ingredients.account_id AS ingredients_account_id
FROM ingredients
WHERE ingredients.account_id = ? AND lower(ingredients.name) = ?
LIMIT ? OFFSET ?

-- Add ingredient row. This query is executed for all ingredients which
-- weren't found by the previous set of queries. The queries are executed
-- separately to retrieve the id generated for each new ingredient.
INSERT INTO ingredients (name, account_id) VALUES (?, ?)

-- Add rows to associate ingredients with the recipe.
INSERT INTO recipe_ingredient (amount, amount_unit, ingredient_id, recipe_id) VALUES (?, ?, ?, ?)
```
*As a user, I want to view individual recipes.*
```sql
-- Get recipe data.
SELECT recipes.id AS recipes_id, recipes.name AS recipes_name, recipes.description AS recipes_description, recipes.steps AS recipes_steps, recipes.account_id AS recipes_account_id
FROM recipes
WHERE recipes.id = ? AND recipes.account_id = ?

-- Get data for ingredients associated with the recipe.
SELECT ri.amount AS amount, ri.amount_unit AS amount_unit, i.id AS id, i.name AS name
FROM ingredients i, recipe_ingredient ri
WHERE
    ri.recipe_id = ?
    AND i.account_id = ?
    AND ri.ingredient_id = i.id

-- Get shopping list amounts for ingredients. This is a separate query from
-- the previous one because both the shopping list and the recipe can have
-- multiple ingredient rows with different amounts and units.
SELECT
    i.id AS id,
    SUM(sli.amount) AS amount,
    sli.amount_unit AS unit
FROM (
    SELECT DISTINCT
        i.id AS id,
        i.name AS name
    FROM ingredients i, recipe_ingredient ri
    WHERE
        i.account_id = ?
        AND i.id = ri.ingredient_id
        AND ri.recipe_id = ?
) i
LEFT JOIN shopping_list_items sli
ON sli.ingredient_id = i.id
WHERE sli.account_id = ?
GROUP BY i.id, sli.amount_unit
```
*As a user, I want to edit recipes.*
```sql
-- Check the recipe exists.
SELECT recipes.id AS recipes_id, recipes.name AS recipes_name, recipes.description AS recipes_description, recipes.steps AS recipes_steps, recipes.account_id AS recipes_account_id
FROM recipes
WHERE recipes.id = ? AND recipes.account_id = ?
LIMIT ? OFFSET ?

-- Update recipe row.
UPDATE recipes SET steps=? WHERE recipes.id = ?

-- Delete existing ingredient associations. Deleting all rows is simpler
-- than trying to determine which should be left.
DELETE FROM recipe_ingredient WHERE recipe_ingredient.recipe_id = ?

-- Check if the ingredient exists. This query is executed for all ingredients
-- in the updated recipe.
SELECT ingredients.id AS ingredients_id, ingredients.name AS ingredients_name, ingredients.account_id AS ingredients_account_id
FROM ingredients
WHERE ingredients.account_id = ? AND lower(ingredients.name) = ?
LIMIT ? OFFSET ?

-- Add ingredient row. This query is executed for all ingredients which
-- weren't found by the previous set of queries. The queries are executed
-- separately to retrieve the id generated for each new ingredient.
INSERT INTO ingredients (name, account_id) VALUES (?, ?)

-- Add rows to associate ingredients with the recipe.
INSERT INTO recipe_ingredient (amount, amount_unit, ingredient_id, recipe_id) VALUES (?, ?, ?, ?)
```
*As a user, I want to delete recipes.*
```sql
-- Delete the recipe row. Associated rows from table recipe_ingredient are
-- deleted by ON DELETE CASCADE constraint on the table.
DELETE FROM recipes WHERE recipes.id = ? AND recipes.account_id = ?

-- Delete ingredients which are not referred to by any recipe or shopping
-- list item.
DELETE FROM ingredients
WHERE ingredients.id IN (
    SELECT i.id FROM ingredients i
    LEFT JOIN recipe_ingredient ri ON ri.ingredient_id = i.id
    LEFT JOIN shopping_list_items sli ON sli.ingredient_id = i.id
    WHERE
        i.account_id = ?
        AND ri.id IS NULL
        AND sli.id IS NULL
)
```
*As a user, I want to search recipes.*
```sql
-- Get recipes matching the search query. The where clause checks against
-- columns name, description and steps depending on the filters used when
-- searching.
SELECT recipes.id AS recipes_id, recipes.name AS recipes_name, recipes.description AS recipes_description, recipes.steps AS recipes_steps, recipes.account_id AS recipes_account_id
FROM recipes
WHERE ((recipes.name LIKE '%' || ? || '%' ESCAPE '/') OR (recipes.description LIKE '%' || ? || '%' ESCAPE '/') OR (recipes.steps LIKE '%' || ? || '%' ESCAPE '/')) AND recipes.account_id = ? ORDER BY recipes.name
LIMIT ? OFFSET ?
```

## Shopping list
*As a user, I want to add ingredients to a shopping list.*
```sql
-- Check the ingredient exists.
SELECT ingredients.id AS ingredients_id, ingredients.name AS ingredients_name, ingredients.account_id AS ingredients_account_id 
FROM ingredients 
WHERE ingredients.account_id = ? AND lower(ingredients.name) = lower(?)
LIMIT ? OFFSET ?

-- Insert the ingredient if it doesn't exist.
INSERT INTO ingredients (name, account_id) VALUES (?, ?)

-- Insert row.
INSERT INTO shopping_list_items (amount, amount_unit, ingredient_id, account_id) VALUES (?, ?, ?, ?)
```
*As a user, I want to edit ingredients in the shopping list.*
```sql
-- Check the item exists.
SELECT shopping_list_items.id AS shopping_list_items_id, shopping_list_items.amount AS shopping_list_items_amount, shopping_list_items.amount_unit AS shopping_list_items_amount_unit, shopping_list_items.ingredient_id AS shopping_list_items_ingredient_id, shopping_list_items.account_id AS shopping_list_items_account_id 
FROM shopping_list_items 
WHERE shopping_list_items.id = ? AND shopping_list_items.account_id = ?
LIMIT ? OFFSET ?

-- Check the ingredient exists.
SELECT ingredients.id AS ingredients_id, ingredients.name AS ingredients_name, ingredients.account_id AS ingredients_account_id 
FROM ingredients 
WHERE ingredients.account_id = ? AND lower(ingredients.name) = lower(?)
LIMIT ? OFFSET ?

-- Insert the ingredient if it doesn't exist.
INSERT INTO ingredients (name, account_id) VALUES (?, ?)

-- Update shopping list row.
UPDATE shopping_list_items SET amount=? WHERE shopping_list_items.id = ?

-- Delete ingredients which are not referred to by any recipe or shopping
-- list item.
DELETE FROM ingredients
WHERE ingredients.id IN (
    SELECT i.id FROM ingredients i
    LEFT JOIN recipe_ingredient ri ON ri.ingredient_id = i.id
    LEFT JOIN shopping_list_items sli ON sli.ingredient_id = i.id
    WHERE
        i.account_id = ?
        AND ri.id IS NULL
        AND sli.id IS NULL
)
```
*As a user, I want to remove ingredients from the shopping list.*
```sql
-- Delete row.
DELETE FROM shopping_list_items WHERE shopping_list_items.id = ? AND shopping_list_items.account_id = ?

-- Delete ingredients which are not referred to by any recipe or shopping
-- list item.
DELETE FROM ingredients
WHERE ingredients.id IN (
    SELECT i.id FROM ingredients i
    LEFT JOIN recipe_ingredient ri ON ri.ingredient_id = i.id
    LEFT JOIN shopping_list_items sli ON sli.ingredient_id = i.id
    WHERE
        i.account_id = ?
        AND ri.id IS NULL
        AND sli.id IS NULL
)
```

## Administration
*As an administrator, I want to search accounts.*
```sql
-- Get accounts matching the search query.
SELECT accounts.id AS accounts_id, accounts.username AS accounts_username, accounts.password_hash AS accounts_password_hash, accounts.role AS accounts_role
FROM accounts
WHERE (accounts.username LIKE '%' || ? || '%' ESCAPE '/') OR (accounts.role LIKE '%' || ? || '%' ESCAPE '/') ORDER BY accounts.username, accounts.id
LIMIT ? OFFSET ?
```
*As an administrator, I want to create new accounts.*
```sql
-- Check for duplicate username.
SELECT EXISTS (SELECT * 
FROM accounts 
WHERE accounts.username = ?) AS anon_1

-- Insert account row.
INSERT INTO accounts (username, password_hash, role) VALUES (?, ?, ?)
```
*As an administrator, I want to edit accounts.*
```sql
-- Check the account exists.
SELECT accounts.id AS accounts_id, accounts.username AS accounts_username, accounts.password_hash AS accounts_password_hash, accounts.role AS accounts_role 
FROM accounts 
WHERE accounts.id = ?
LIMIT ? OFFSET ?

-- Check for duplicate username.
SELECT accounts.id AS accounts_id, accounts.username AS accounts_username, accounts.password_hash AS accounts_password_hash, accounts.role AS accounts_role
FROM accounts
WHERE accounts.username = ?
LIMIT ? OFFSET ?

-- Update account row.
UPDATE accounts SET password_hash=? WHERE accounts.id = ?
```
*As an administrator, I want to remove accounts.*
```sql
-- Delete account row.
DELETE FROM accounts WHERE accounts.id = ?
```
