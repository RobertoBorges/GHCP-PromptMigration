using System;
using System.Collections.Generic;
using System.Text;
using System.Data;
using System.Data.SqlClient;
using BookShop.Common.Models;
using BookShop.DataAccess.Base;

namespace BookShop.DataAccess.Repositories
{
    public class BookRepository : BaseRepository
    {
        public List<Book> GetAllBooks()
        {
            string query = @"
                SELECT b.BookId, b.Title, b.ISBN, b.Description, b.Price, b.StockQuantity, 
                       b.PublicationDate, b.ImageUrl, b.IsActive, b.CreatedDate, b.ModifiedDate,
                       b.AuthorId, b.CategoryId,
                       a.FirstName as AuthorFirstName, a.LastName as AuthorLastName,
                       c.Name as CategoryName
                FROM Books b
                INNER JOIN Authors a ON b.AuthorId = a.AuthorId
                INNER JOIN Categories c ON b.CategoryId = c.CategoryId
                WHERE b.IsActive = 1
                ORDER BY b.Title";

            DataTable dataTable = ExecuteQuery(query);
            return ConvertDataTableToBooks(dataTable);
        }

        public Book GetBookById(int bookId)
        {
            string query = @"
                SELECT b.BookId, b.Title, b.ISBN, b.Description, b.Price, b.StockQuantity, 
                       b.PublicationDate, b.ImageUrl, b.IsActive, b.CreatedDate, b.ModifiedDate,
                       b.AuthorId, b.CategoryId,
                       a.FirstName as AuthorFirstName, a.LastName as AuthorLastName,
                       c.Name as CategoryName
                FROM Books b
                INNER JOIN Authors a ON b.AuthorId = a.AuthorId
                INNER JOIN Categories c ON b.CategoryId = c.CategoryId
                WHERE b.BookId = @BookId";

            SqlParameter[] parameters = { CreateParameter("@BookId", bookId) };
            DataTable dataTable = ExecuteQuery(query, parameters);
            
            List<Book> books = ConvertDataTableToBooks(dataTable);
            return books.Count > 0 ? books[0] : null;
        }

        public List<Book> GetBooksByCategory(int categoryId)
        {
            string query = @"
                SELECT b.BookId, b.Title, b.ISBN, b.Description, b.Price, b.StockQuantity, 
                       b.PublicationDate, b.ImageUrl, b.IsActive, b.CreatedDate, b.ModifiedDate,
                       b.AuthorId, b.CategoryId,
                       a.FirstName as AuthorFirstName, a.LastName as AuthorLastName,
                       c.Name as CategoryName
                FROM Books b
                INNER JOIN Authors a ON b.AuthorId = a.AuthorId
                INNER JOIN Categories c ON b.CategoryId = c.CategoryId
                WHERE b.CategoryId = @CategoryId AND b.IsActive = 1
                ORDER BY b.Title";

            SqlParameter[] parameters = { CreateParameter("@CategoryId", categoryId) };
            DataTable dataTable = ExecuteQuery(query, parameters);
            return ConvertDataTableToBooks(dataTable);
        }

        public int InsertBook(Book book)
        {
            string query = @"
                INSERT INTO Books (Title, ISBN, Description, Price, StockQuantity, PublicationDate, 
                                 ImageUrl, IsActive, AuthorId, CategoryId, CreatedDate, ModifiedDate)
                VALUES (@Title, @ISBN, @Description, @Price, @StockQuantity, @PublicationDate, 
                        @ImageUrl, @IsActive, @AuthorId, @CategoryId, @CreatedDate, @ModifiedDate);
                SELECT SCOPE_IDENTITY();";

            SqlParameter[] parameters = {
                CreateParameter("@Title", book.Title),
                CreateParameter("@ISBN", book.ISBN),
                CreateParameter("@Description", book.Description),
                CreateParameter("@Price", book.Price),
                CreateParameter("@StockQuantity", book.StockQuantity),
                CreateParameter("@PublicationDate", book.PublicationDate),
                CreateParameter("@ImageUrl", book.ImageUrl),
                CreateParameter("@IsActive", book.IsActive),
                CreateParameter("@AuthorId", book.AuthorId),
                CreateParameter("@CategoryId", book.CategoryId),
                CreateParameter("@CreatedDate", DateTime.Now),
                CreateParameter("@ModifiedDate", DateTime.Now)
            };

            object result = ExecuteScalar(query, parameters);
            return Convert.ToInt32(result);
        }

        public bool UpdateBook(Book book)
        {
            string query = @"
                UPDATE Books 
                SET Title = @Title, ISBN = @ISBN, Description = @Description, Price = @Price, 
                    StockQuantity = @StockQuantity, PublicationDate = @PublicationDate,
                    ImageUrl = @ImageUrl, IsActive = @IsActive, AuthorId = @AuthorId, 
                    CategoryId = @CategoryId, ModifiedDate = @ModifiedDate
                WHERE BookId = @BookId";

            SqlParameter[] parameters = {
                CreateParameter("@BookId", book.BookId),
                CreateParameter("@Title", book.Title),
                CreateParameter("@ISBN", book.ISBN),
                CreateParameter("@Description", book.Description),
                CreateParameter("@Price", book.Price),
                CreateParameter("@StockQuantity", book.StockQuantity),
                CreateParameter("@PublicationDate", book.PublicationDate),
                CreateParameter("@ImageUrl", book.ImageUrl),
                CreateParameter("@IsActive", book.IsActive),
                CreateParameter("@AuthorId", book.AuthorId),
                CreateParameter("@CategoryId", book.CategoryId),
                CreateParameter("@ModifiedDate", DateTime.Now)
            };

            return ExecuteNonQuery(query, parameters) > 0;
        }

        public bool DeleteBook(int bookId)
        {
            string query = "UPDATE Books SET IsActive = 0, ModifiedDate = @ModifiedDate WHERE BookId = @BookId";
            SqlParameter[] parameters = {
                CreateParameter("@BookId", bookId),
                CreateParameter("@ModifiedDate", DateTime.Now)
            };

            return ExecuteNonQuery(query, parameters) > 0;
        }

        private List<Book> ConvertDataTableToBooks(DataTable dataTable)
        {
            List<Book> books = new List<Book>();

            foreach (DataRow row in dataTable.Rows)
            {
                Book book = new Book
                {
                    BookId = Convert.ToInt32(row["BookId"]),
                    Title = row["Title"].ToString(),
                    ISBN = row["ISBN"].ToString(),
                    Description = row["Description"].ToString(),
                    Price = Convert.ToDecimal(row["Price"]),
                    StockQuantity = Convert.ToInt32(row["StockQuantity"]),
                    PublicationDate = Convert.ToDateTime(row["PublicationDate"]),
                    ImageUrl = row["ImageUrl"].ToString(),
                    IsActive = Convert.ToBoolean(row["IsActive"]),
                    CreatedDate = Convert.ToDateTime(row["CreatedDate"]),
                    ModifiedDate = Convert.ToDateTime(row["ModifiedDate"]),
                    AuthorId = Convert.ToInt32(row["AuthorId"]),
                    CategoryId = Convert.ToInt32(row["CategoryId"]),
                    Author = new Author
                    {
                        AuthorId = Convert.ToInt32(row["AuthorId"]),
                        FirstName = row["AuthorFirstName"].ToString(),
                        LastName = row["AuthorLastName"].ToString()
                    },
                    Category = new Category
                    {
                        CategoryId = Convert.ToInt32(row["CategoryId"]),
                        Name = row["CategoryName"].ToString()
                    }
                };

                books.Add(book);
            }

            return books;
        }
    }
}