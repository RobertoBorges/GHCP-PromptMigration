-- BookShop Database Creation Script
-- Compatible with SQL Server 2008
-- Created: 2008

USE master;
GO

-- Drop database if exists
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'BookShopDB')
BEGIN
    ALTER DATABASE BookShopDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE BookShopDB;
END
GO

-- Create database
CREATE DATABASE BookShopDB
ON 
( NAME = 'BookShopDB_Data',
  FILENAME = '/var/opt/mssql/data/BookShopDB.mdf',
  SIZE = 100MB,
  MAXSIZE = 1GB,
  FILEGROWTH = 10MB )
LOG ON 
( NAME = 'BookShopDB_Log',
  FILENAME = '/var/opt/mssql/data/BookShopDB.ldf',
  SIZE = 10MB,
  MAXSIZE = 100MB,
  FILEGROWTH = 1MB );
GO

USE BookShopDB;
GO

-- Create Authors table
CREATE TABLE Authors (
    AuthorId int IDENTITY(1,1) PRIMARY KEY,
    FirstName nvarchar(50) NOT NULL,
    LastName nvarchar(50) NOT NULL,
    Biography nvarchar(max) NULL,
    BirthDate datetime NULL,
    Nationality nvarchar(50) NULL,
    PhotoUrl nvarchar(255) NULL,
    IsActive bit NOT NULL DEFAULT 1,
    CreatedDate datetime NOT NULL DEFAULT GETDATE(),
    ModifiedDate datetime NOT NULL DEFAULT GETDATE()
);

-- Create Categories table
CREATE TABLE Categories (
    CategoryId int IDENTITY(1,1) PRIMARY KEY,
    Name nvarchar(100) NOT NULL,
    Description nvarchar(500) NULL,
    IsActive bit NOT NULL DEFAULT 1,
    CreatedDate datetime NOT NULL DEFAULT GETDATE(),
    ModifiedDate datetime NOT NULL DEFAULT GETDATE()
);

-- Create Books table
CREATE TABLE Books (
    BookId int IDENTITY(1,1) PRIMARY KEY,
    Title nvarchar(255) NOT NULL,
    ISBN nvarchar(20) NOT NULL,
    Description nvarchar(max) NULL,
    Price decimal(10,2) NOT NULL,
    StockQuantity int NOT NULL DEFAULT 0,
    PublicationDate datetime NULL,
    ImageUrl nvarchar(255) NULL,
    IsActive bit NOT NULL DEFAULT 1,
    AuthorId int NOT NULL,
    CategoryId int NOT NULL,
    CreatedDate datetime NOT NULL DEFAULT GETDATE(),
    ModifiedDate datetime NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT FK_Books_Authors FOREIGN KEY (AuthorId) REFERENCES Authors(AuthorId),
    CONSTRAINT FK_Books_Categories FOREIGN KEY (CategoryId) REFERENCES Categories(CategoryId)
);

-- Create Customers table
CREATE TABLE Customers (
    CustomerId int IDENTITY(1,1) PRIMARY KEY,
    FirstName nvarchar(50) NOT NULL,
    LastName nvarchar(50) NOT NULL,
    Email nvarchar(100) NOT NULL,
    Phone nvarchar(20) NULL,
    Address nvarchar(255) NULL,
    City nvarchar(50) NULL,
    State nvarchar(50) NULL,
    ZipCode nvarchar(10) NULL,
    Country nvarchar(50) NULL DEFAULT 'USA',
    IsActive bit NOT NULL DEFAULT 1,
    CreatedDate datetime NOT NULL DEFAULT GETDATE(),
    ModifiedDate datetime NOT NULL DEFAULT GETDATE()
);

-- Create Employees table  
CREATE TABLE Employees (
    EmployeeId int IDENTITY(1,1) PRIMARY KEY,
    FirstName nvarchar(50) NOT NULL,
    LastName nvarchar(50) NOT NULL,
    Email nvarchar(100) NOT NULL,
    Phone nvarchar(20) NULL,
    Position nvarchar(100) NOT NULL,
    Department nvarchar(50) NOT NULL,
    HireDate datetime NOT NULL,
    Salary decimal(10,2) NOT NULL,
    IsActive bit NOT NULL DEFAULT 1,
    IsAdmin bit NOT NULL DEFAULT 0,
    WindowsUsername nvarchar(100) NOT NULL,
    CreatedDate datetime NOT NULL DEFAULT GETDATE(),
    ModifiedDate datetime NOT NULL DEFAULT GETDATE()
);

-- Create Orders table
CREATE TABLE Orders (
    OrderId int IDENTITY(1,1) PRIMARY KEY,
    OrderDate datetime NOT NULL DEFAULT GETDATE(),
    TotalAmount decimal(10,2) NOT NULL,
    Status nvarchar(50) NOT NULL DEFAULT 'Pending',
    ShippingAddress nvarchar(500) NULL,
    BillingAddress nvarchar(500) NULL,
    ShippedDate datetime NULL,
    TrackingNumber nvarchar(100) NULL,
    CustomerId int NOT NULL,
    EmployeeId int NULL,
    CreatedDate datetime NOT NULL DEFAULT GETDATE(),
    ModifiedDate datetime NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId),
    CONSTRAINT FK_Orders_Employees FOREIGN KEY (EmployeeId) REFERENCES Employees(EmployeeId)
);

-- Create OrderItems table
CREATE TABLE OrderItems (
    OrderItemId int IDENTITY(1,1) PRIMARY KEY,
    Quantity int NOT NULL,
    UnitPrice decimal(10,2) NOT NULL,
    TotalPrice decimal(10,2) NOT NULL,
    OrderId int NOT NULL,
    BookId int NOT NULL,
    CreatedDate datetime NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT FK_OrderItems_Orders FOREIGN KEY (OrderId) REFERENCES Orders(OrderId),
    CONSTRAINT FK_OrderItems_Books FOREIGN KEY (BookId) REFERENCES Books(BookId)
);

-- Create Indexes for performance
CREATE INDEX IX_Books_AuthorId ON Books(AuthorId);
CREATE INDEX IX_Books_CategoryId ON Books(CategoryId);
CREATE INDEX IX_Books_IsActive ON Books(IsActive);
CREATE INDEX IX_Orders_CustomerId ON Orders(CustomerId);
CREATE INDEX IX_Orders_EmployeeId ON Orders(EmployeeId);
CREATE INDEX IX_OrderItems_OrderId ON OrderItems(OrderId);
CREATE INDEX IX_OrderItems_BookId ON OrderItems(BookId);
CREATE INDEX IX_Employees_WindowsUsername ON Employees(WindowsUsername);

PRINT 'BookShop database created successfully!';
GO