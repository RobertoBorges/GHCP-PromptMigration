-- BookShop Database Population Script
-- Sample data for testing and demonstration
-- Compatible with SQL Server 2008

USE BookShopDB;
GO

-- Reset the identity value for the Books table
DBCC CHECKIDENT ('Books', RESEED, 0);

-- Reset the identity for other tables
DBCC CHECKIDENT ('Authors', RESEED, 0);
DBCC CHECKIDENT ('Categories', RESEED, 0);
DBCC CHECKIDENT ('Customers', RESEED, 0);
DBCC CHECKIDENT ('Employees', RESEED, 0);
DBCC CHECKIDENT ('Orders', RESEED, 0);
DBCC CHECKIDENT ('OrderItems', RESEED, 0);

-- Insert Categories
INSERT INTO Categories (Name, Description) VALUES
('Fiction', 'Fictional literature including novels and short stories'),
('Non-Fiction', 'Factual books including biographies, history, and science'),
('Science Fiction', 'Science fiction and fantasy literature'),
('Mystery', 'Mystery and thriller novels'),
('Romance', 'Romance novels and love stories'),
('Biography', 'Biographies and autobiographies'),
('History', 'Historical books and documentaries'),
('Technology', 'Computer science and technology books'),
('Business', 'Business and management books'),
('Self-Help', 'Personal development and self-improvement books');

-- Insert Authors
INSERT INTO Authors (FirstName, LastName, Biography, BirthDate, Nationality) VALUES
('J.K.', 'Rowling', 'British author best known for the Harry Potter series', '1965-07-31', 'British'),
('Stephen', 'King', 'American author of horror, supernatural fiction, suspense, and fantasy novels', '1947-09-21', 'American'),
('Agatha', 'Christie', 'British crime writer known for her detective novels', '1890-09-15', 'British'),
('Isaac', 'Asimov', 'American writer and professor of biochemistry, known for science fiction', '1920-01-02', 'American'),
('Jane', 'Austen', 'English novelist known for her romantic fiction', '1775-12-16', 'British'),
('Mark', 'Twain', 'American writer and humorist', '1835-11-30', 'American'),
('Ernest', 'Hemingway', 'American novelist and short story writer', '1899-07-21', 'American'),
('George', 'Orwell', 'British author and journalist', '1903-06-25', 'British'),
('William', 'Shakespeare', 'English playwright and poet', '1864-04-26', 'British'),
('Charles', 'Dickens', 'British writer and social critic', '1812-02-07', 'British');

-- Insert Books
INSERT INTO Books (Title, ISBN, Description, Price, StockQuantity, PublicationDate, AuthorId, CategoryId, ImageUrl) VALUES
('Harry Potter and the Philosopher''s Stone', '978-0747532699', 'The first book in the Harry Potter series', 12.99, 50, '1997-06-26', 1, 1, '/images/books/harry-potter-1.jpg'),
('Harry Potter and the Chamber of Secrets', '978-0747538493', 'The second book in the Harry Potter series', 12.99, 45, '1998-07-02', 1, 1, '/images/books/harry-potter-2.jpg'),
('The Shining', '978-0307743657', 'A psychological horror novel', 14.99, 30, '1977-01-28', 2, 4, '/images/books/the-shining.jpg'),
('It', '978-1501142970', 'A horror novel about a creature that preys on children', 16.99, 25, '1986-09-15', 2, 4, '/images/books/it.jpg'),
('Murder on the Orient Express', '978-0062693662', 'A famous detective novel featuring Hercule Poirot', 13.99, 40, '1934-01-01', 3, 4, '/images/books/orient-express.jpg'),
('The ABC Murders', '978-0062074003', 'Another Hercule Poirot mystery', 12.99, 35, '1936-01-06', 3, 4, '/images/books/abc-murders.jpg'),
('Foundation', '978-0553293357', 'First book in the Foundation series', 15.99, 20, '1951-05-01', 4, 3, '/images/books/foundation.jpg'),
('I, Robot', '978-0553294385', 'Collection of science fiction short stories', 13.99, 28, '1950-12-02', 4, 3, '/images/books/i-robot.jpg'),
('Pride and Prejudice', '978-0141439518', 'Classic romance novel', 11.99, 60, '1813-01-28', 5, 5, '/images/books/pride-prejudice.jpg'),
('Sense and Sensibility', '978-0141439662', 'Another classic by Jane Austen', 11.99, 55, '1811-10-30', 5, 5, '/images/books/sense-sensibility.jpg'),
('The Adventures of Tom Sawyer', '978-0486400778', 'Classic American literature', 10.99, 42, '1876-01-01', 6, 1, '/images/books/tom-sawyer.jpg'),
('The Old Man and the Sea', '978-0684801223', 'Pulitzer Prize winning novella', 12.99, 38, '1952-09-01', 7, 1, '/images/books/old-man-sea.jpg'),
('1984', '978-0452284234', 'Dystopian social science fiction novel', 13.99, 65, '1949-06-08', 8, 1, '/images/books/1984.jpg'),
('Animal Farm', '978-0452284240', 'Allegorical novella', 10.99, 70, '1945-08-17', 8, 1, '/images/books/animal-farm.jpg'),
('Romeo and Juliet', '978-0486275437', 'Classic tragedy play', 9.99, 80, '1897-01-01', 9, 1, '/images/books/romeo-juliet.jpg'),
('Hamlet', '978-0486272788', 'Famous tragedy play', 9.99, 75, '1803-01-01', 9, 1, '/images/books/hamlet.jpg'),
('A Christmas Carol', '978-0486268651', 'Classic Christmas story', 8.99, 90, '1843-12-19', 10, 1, '/images/books/christmas-carol.jpg'),
('Great Expectations', '978-0486415864', 'Coming-of-age novel', 12.99, 48, '1861-08-01', 10, 1, '/images/books/great-expectations.jpg');

-- Insert Employees (for Windows Authentication)
INSERT INTO Employees (FirstName, LastName, Email, Phone, Position, Department, HireDate, Salary, IsAdmin, WindowsUsername) VALUES
('John', 'Smith', 'john.smith@bookshop.com', '555-0101', 'Store Manager', 'Management', '2005-01-15', 55000.00, 1, 'BOOKSHOP\jsmith'),
('Mary', 'Johnson', 'mary.johnson@bookshop.com', '555-0102', 'Assistant Manager', 'Management', '2006-03-20', 45000.00, 1, 'BOOKSHOP\mjohnson'),
('Robert', 'Williams', 'robert.williams@bookshop.com', '555-0103', 'Sales Associate', 'Sales', '2007-06-10', 32000.00, 0, 'BOOKSHOP\rwilliams'),
('Linda', 'Brown', 'linda.brown@bookshop.com', '555-0104', 'Sales Associate', 'Sales', '2007-09-15', 32000.00, 0, 'BOOKSHOP\lbrown'),
('James', 'Davis', 'james.davis@bookshop.com', '555-0105', 'Inventory Specialist', 'Operations', '2008-02-01', 35000.00, 0, 'BOOKSHOP\jdavis'),
('Patricia', 'Miller', 'patricia.miller@bookshop.com', '555-0106', 'Customer Service', 'Sales', '2008-04-12', 30000.00, 0, 'BOOKSHOP\pmiller');

-- Insert Sample Customers
INSERT INTO Customers (FirstName, LastName, Email, Phone, Address, City, State, ZipCode) VALUES
('Alice', 'Anderson', 'alice.anderson@email.com', '555-1001', '123 Main St', 'Springfield', 'IL', '62701'),
('Bob', 'Baker', 'bob.baker@email.com', '555-1002', '456 Oak Ave', 'Springfield', 'IL', '62702'),
('Carol', 'Clark', 'carol.clark@email.com', '555-1003', '789 Pine Rd', 'Springfield', 'IL', '62703'),
('David', 'Evans', 'david.evans@email.com', '555-1004', '321 Elm St', 'Springfield', 'IL', '62704'),
('Emma', 'Foster', 'emma.foster@email.com', '555-1005', '654 Maple Dr', 'Springfield', 'IL', '62705');

-- Insert Sample Orders
INSERT INTO Orders (OrderDate, TotalAmount, Status, ShippingAddress, BillingAddress, CustomerId, EmployeeId) VALUES
('2008-01-15', 25.98, 'Completed', '123 Main St, Springfield, IL 62701', '123 Main St, Springfield, IL 62701', 1, 3),
('2008-01-16', 42.97, 'Shipped', '456 Oak Ave, Springfield, IL 62702', '456 Oak Ave, Springfield, IL 62702', 2, 4),
('2008-01-17', 13.99, 'Processing', '789 Pine Rd, Springfield, IL 62703', '789 Pine Rd, Springfield, IL 62703', 3, 3),
('2008-01-18', 29.98, 'Completed', '321 Elm St, Springfield, IL 62704', '321 Elm St, Springfield, IL 62704', 4, 4),
('2008-01-19', 18.98, 'Pending', '654 Maple Dr, Springfield, IL 62705', '654 Maple Dr, Springfield, IL 62705', 5, 3);

-- Insert Sample Order Items
INSERT INTO OrderItems (Quantity, UnitPrice, TotalPrice, OrderId, BookId) VALUES
(2, 12.99, 25.98, 1, 1),
(1, 14.99, 14.99, 2, 3),
(1, 13.99, 13.99, 2, 5),
(1, 15.99, 15.99, 2, 7),
(1, 13.99, 13.99, 3, 13),
(1, 11.99, 11.99, 4, 9),
(1, 12.99, 12.99, 4, 18),
(2, 9.99, 19.98, 5, 15);

PRINT 'Sample data inserted successfully!';
GO