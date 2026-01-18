use assign1_clean;
DELETE FROM bookstore_cartitem WHERE ID>0;
DELETE FROM bookstore_cart WHERE ID>0;
DELETE FROM bookstore_book WHERE ID>0;
INSERT INTO bookstore_book VALUES(0, "Ngu Van 6", 10, "ABC", 50);
INSERT INTO bookstore_book VALUES(0, "Toan 7", 20, "DEF", 40);
INSERT INTO bookstore_book VALUES(0, "Vat Ly 8", 30, "GHI", 60);

use assign1_micro_cart;
DELETE FROM cart_cartitem WHERE ID>0;
DELETE FROM cart_cart WHERE ID>0;
use assign1_micro_book;
DELETE FROM book_book WHERE ID>0;
INSERT INTO book_book VALUES(0, "Ngu Van 6", 10, "ABC", 50);
INSERT INTO book_book VALUES(0, "Toan 7", 20, "DEF", 40);
INSERT INTO book_book VALUES(0, "Vat Ly 8", 30, "GHI", 60);

use assign1_monolith;
INSERT INTO bookstore_book VALUES(0, "Ngu Van 6", "ABC", 10, 50);
INSERT INTO bookstore_book VALUES(0, "Toan 7", "DEF", 20, 40);
INSERT INTO bookstore_book VALUES(0, "Vat Ly 8", "GHI", 30, 60);

