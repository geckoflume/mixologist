-- DROP DATABASE IF EXISTS mixologist;
-- CREATE DATABASE mixologist;
ALTER DATABASE mixologist CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin;

DROP TABLE IF EXISTS glass;
DROP TABLE IF EXISTS bottles;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS recipes_ingredient_rel;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS ingredients;

CREATE TABLE ingredients
(
    id      int(11) PRIMARY KEY AUTO_INCREMENT,
    name    varchar(255) NOT NULL,
    alcohol boolean      NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE utf8mb4_bin;

CREATE TABLE glass
(
    id            int(11) PRIMARY KEY AUTO_INCREMENT,
    capacity      int(11) NOT NULL,
    actual_volume int(11) NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE utf8mb4_bin;

CREATE TABLE bottles
(
    id            int(11) PRIMARY KEY AUTO_INCREMENT,
    name          varchar(255) NOT NULL,
    ingredient_id int(11)      NOT NULL,
    capacity      int(11)      NOT NULL,
    actual_volume int(11)      NOT NULL,
    enabled       boolean      NOT NULL,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE utf8mb4_bin;

CREATE TABLE recipes
(
    id    int(11) PRIMARY KEY AUTO_INCREMENT,
    name  varchar(255) NOT NULL,
    notes varchar(255) NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE utf8mb4_bin;

CREATE TABLE recipes_ingredient_rel
(
    recipe_id     int(11),
    ingredient_id int(11),
    quantity      int(11),
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE utf8mb4_bin;

CREATE TABLE history
(
    id        int(11) PRIMARY KEY AUTO_INCREMENT,
    recipe_id int(11),
    made_at   timestamp,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE utf8mb4_bin;


INSERT INTO ingredients (id, name, alcohol)
VALUES (1, 'Flat Water', 0),
       (2, 'Sugar syrup', 0),
       (3, 'Lime juice', 0),
       (4, 'Lemon juice', 0),
       (5, 'London dry gin', 1),
       (6, 'Vodka', 1),
       (7, 'Light white rum', 1),
       (8, 'Angostura Aromatic Bitters', 1),
       (9, 'Orange juice', 0),
       (10, 'Triple sec liqueur', 1),
       (11, 'Dry vermouth', 1),
       (12, 'Cognac V.S.O.P.', 1),
       (13, 'Pineapple juice', 0),
       (14, 'Sweet vermouth', 1),
       (15, 'Bourbon whiskey', 1),
       (16, 'Apple juice', 0),
       (17, 'Pomegranate (grenadine) syrup', 0),
       (18, 'Tequila (reposado)', 1),
       (19, 'Egg white', 0),
       (20, 'Orange bitters', 1),
       (21, 'Cranberry juice (red)', 0),
       (22, 'Grand Marnier liqueur', 1),
       (23, 'Soda (club soda)', 0),
       (24, 'Cream', 0),
       (25, 'Maraschino liqueur', 1),
       (26, 'Blended Scotch whisky', 1),
       (27, 'Fresh mint leaves/sprigs', 0),
       (28, 'Brut champagne', 1),
       (29, 'Grapefruit juice (pink)', 0),
       (30, 'Elderflower liqueur', 1),
       (31, 'Absinthe', 1),
       (32, 'Apricot brandy liqueur', 1),
       (33, 'Coffee liqueur', 1),
       (34, 'Campari Bitter', 1),
       (35, 'Calvados apple brandy', 1),
       (36, 'Amaretto liqueur', 1),
       (37, 'Milk', 0),
       (38, 'Black raspberry liqueur', 1),
       (39, 'Runny honey', 0),
       (40, 'Bénédictine D.O.M. liqueur', 1),
       (41, 'White crème de cacao liqueur', 1),
       (42, 'Peychaud\'s aromatic bitters', 1),
       (43, 'Aged rum (+7 year old)', 1),
       (44, 'Citrus flavoured vodka', 1),
       (45, 'Chartreuse Vert (green)', 1),
       (46, 'Cherry brandy liqueur', 1),
       (47, 'Irish cream liqueur', 1),
       (48, 'Almond (orgeat) syrup', 0),
       (49, 'Cachaça', 1),
       (50, 'Lime cordial', 0),
       (51, 'Raspberries (fresh)', 0),
       (52, 'Golden rum', 1),
       (53, 'Ginger ale', 1),
       (54, 'Crème de cassis', 1),
       (55, 'Melon liqueur (green)', 1),
       (56, 'Galliano L\'Autentico liqueur', 1),
       (57, 'Blue curaçao liqueur', 1),
       (58, 'Drambuie liqueur', 1),
       (59, 'Vanilla infused vodka', 1),
       (60, 'Straight rye whiskey', 1),
       (61, 'Hazelnut liqueur', 1),
       (62, 'Żubrówka bison grass vodka', 1),
       (63, 'Fino sherry', 1),
       (64, 'Maple syrup', 0),
       (65, 'Islay single malt Scotch whisky', 1),
       (66, 'Agave syrup', 0),
       (67, 'Chartreuse Jaune (yellow)', 1),
       (68, 'Peach Schnapps liqueur', 1),
       (69, 'Crème de banane liqueur', 1),
       (70, 'Port wine', 1),
       (71, 'White wine (Sauvignon Blanc)', 1),
       (72, 'Pisco', 1),
       (73, 'Apple schnapps liqueur', 1),
       (74, 'Ginger beer', 1),
       (75, 'Falernum liqueur', 1),
       (76, 'Lemonade/Sprite/7-Up', 0),
       (77, 'Coconut rum liqueur', 1),
       (78, 'White crème de menthe', 1),
       (79, 'Ginger liqueur', 1),
       (80, 'Southern Comfort liqueur', 1),
       (81, 'Dark crème de cacao liqueur', 1),
       (82, 'Basil leaves', 0),
       (83, 'Dubonnet Red', 1),
       (84, 'Passion fruit syrup', 0),
       (85, 'Jenever', 1),
       (86, 'Vodka raspberry flavoured', 1),
       (87, 'Sake', 1),
       (88, 'Overproof rum (white)', 1),
       (89, 'Strawberries (fresh)', 0),
       (90, 'Ginger (fresh root)', 0),
       (91, 'Navy rum', 1),
       (92, 'Prosecco sparkling wine', 1),
       (93, 'Vanilla sugar syrup', 0),
       (94, 'Passion fruit (fresh)', 0),
       (95, 'Lillet Blanc', 1),
       (96, 'Honey sugar syrup', 0),
       (97, 'Espresso coffee (freshly made)', 0),
       (98, 'Black pepper', 0),
       (99, 'Tonic water', 0),
       (100, 'Anise liqueur', 1),
       (101, 'Crème de framboise liqueur', 1);

INSERT INTO glass (id, capacity, actual_volume)
VALUES (1, 300, 0);

INSERT INTO bottles (id, name, ingredient_id, capacity, actual_volume, enabled)
VALUES (1, '', 1, 700, 0, 0),
       (2, '', 1, 700, 0, 0),
       (3, '', 1, 700, 0, 0),
       (4, '', 1, 700, 0, 0);