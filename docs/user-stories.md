# User stories

*As a user, I want to save recipes for later use.*
- SQL query:
  ```
  INSERT INTO recipes (name, description, steps, account_id)
  VALUES (?, ?, ?, ?);

  SELECT
      ingredients.id AS ingredients_id,
      ingredients.name AS ingredients_name,
      ingredients.account_id AS ingredients_account_id
  FROM ingredients
  WHERE ingredients.account_id = ? AND lower(ingredients.name) = ?
  LIMIT ? OFFSET ?;

  INSERT INTO ingredients (name, account_id)
  VALUES (?, ?);

  INSERT INTO recipe_ingredient (amount, amount_unit, ingredient_id, recipe_id)    
  VALUES (?, ?, ?, ?);
  ```

*As a user, I want to modify existing recipes.*
- SQL query:
  ```
  SELECT
      recipes.id AS recipes_id,
      recipes.name AS recipes_name,
      recipes.description AS recipes_description,
      recipes.steps AS recipes_steps,
      recipes.account_id AS recipes_account_id 
  FROM recipes 
  WHERE recipes.id = ? AND recipes.account_id = ?
  LIMIT ? OFFSET ?;

  UPDATE recipes SET steps=? WHERE recipes.id = ?;

  DELETE FROM recipe_ingredient WHERE recipe_ingredient.recipe_id = ?;

  DELETE FROM ingredients
  WHERE ingredients.id IN (
      SELECT i.id FROM ingredients i
      LEFT JOIN recipe_ingredient ri ON ri.ingredient_id = i.id
      LEFT JOIN shopping_list_items sli ON sli.ingredient_id = i.id
      WHERE
          i.account_id = ?
          AND ri.id IS NULL
          AND sli.id IS NULL
  );
  ```

*As a user, I want to discard excess recipes.*
- SQL query:
  ```
  DELETE FROM recipes
  WHERE recipes.id = ? AND recipes.account_id = ?;

  DELETE FROM ingredients
  WHERE ingredients.id IN (
      SELECT i.id FROM ingredients i
      LEFT JOIN recipe_ingredient ri ON ri.ingredient_id = i.id
      LEFT JOIN shopping_list_items sli ON sli.ingredient_id = i.id
      WHERE
          i.account_id = ?
          AND ri.id IS NULL
          AND sli.id IS NULL
  );
  ```

*As a user, I want to add ingredients to my shopping list.*
- SQL query:
  ```
  SELECT
      shopping_list_items.id AS shopping_list_items_id,
      shopping_list_items.amount AS shopping_list_items_amount,
      shopping_list_items.amount_unit AS shopping_list_items_amount_unit,
      shopping_list_items.ingredient_id AS shopping_list_items_ingredient_id,
      shopping_list_items.account_id AS shopping_list_items_account_id 
  FROM shopping_list_items 
  WHERE
      shopping_list_items.account_id = ?
      AND shopping_list_items.ingredient_id = ?
      AND shopping_list_items.amount_unit = ?
  LIMIT ? OFFSET ?;

  INSERT INTO shopping_list_items (amount, amount_unit, ingredient_id, account_id)
  VALUES (?, ?, ?, ?);
  ```

*As a user, I want to be able to change my password.*
- SQL query
  ```
  UPDATE accounts SET password_hash = ? WHERE accounts.id = ?;
  ```
