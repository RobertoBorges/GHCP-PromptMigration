using System;
using System.Collections.Generic;
using System.Text;
using BookShop.Common.Models;
using BookShop.DataAccess.Repositories;

namespace BookShop.BusinessLogic.Services
{
    public class BookService
    {
        private readonly BookRepository _bookRepository;
        private readonly AuthorRepository _authorRepository;
        private readonly CategoryRepository _categoryRepository;

        public BookService()
        {
            _bookRepository = new BookRepository();
            _authorRepository = new AuthorRepository();
            _categoryRepository = new CategoryRepository();
        }

        public List<Book> GetAllBooks()
        {
            try
            {
                return _bookRepository.GetAllBooks();
            }
            catch (Exception ex)
            {
                // Log error (in a real application, use a proper logging framework)
                throw new ApplicationException("Error retrieving books: " + ex.Message, ex);
            }
        }

        public Book GetBookById(int bookId)
        {
            if (bookId <= 0)
                throw new ArgumentException("Book ID must be greater than zero", "bookId");

            try
            {
                return _bookRepository.GetBookById(bookId);
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error retrieving book: " + ex.Message, ex);
            }
        }

        public List<Book> GetBooksByCategory(int categoryId)
        {
            if (categoryId <= 0)
                throw new ArgumentException("Category ID must be greater than zero", "categoryId");

            try
            {
                return _bookRepository.GetBooksByCategory(categoryId);
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error retrieving books by category: " + ex.Message, ex);
            }
        }

        public bool AddBook(Book book)
        {
            if (book == null)
                throw new ArgumentNullException("book");

            if (string.IsNullOrEmpty(book.Title))
                throw new ArgumentException("Book title is required", "book.Title");

            if (string.IsNullOrEmpty(book.ISBN))
                throw new ArgumentException("Book ISBN is required", "book.ISBN");

            if (book.Price <= 0)
                throw new ArgumentException("Book price must be greater than zero", "book.Price");

            try
            {
                int bookId = _bookRepository.InsertBook(book);
                return bookId > 0;
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error adding book: " + ex.Message, ex);
            }
        }

        public bool UpdateBook(Book book)
        {
            if (book == null)
                throw new ArgumentNullException("book");

            if (book.BookId <= 0)
                throw new ArgumentException("Book ID must be greater than zero", "book.BookId");

            try
            {
                return _bookRepository.UpdateBook(book);
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error updating book: " + ex.Message, ex);
            }
        }

        public bool DeleteBook(int bookId)
        {
            if (bookId <= 0)
                throw new ArgumentException("Book ID must be greater than zero", "bookId");

            try
            {
                return _bookRepository.DeleteBook(bookId);
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error deleting book: " + ex.Message, ex);
            }
        }

        public List<Author> GetAllAuthors()
        {
            try
            {
                return _authorRepository.GetAllAuthors();
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error retrieving authors: " + ex.Message, ex);
            }
        }

        public List<Category> GetAllCategories()
        {
            try
            {
                return _categoryRepository.GetAllCategories();
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error retrieving categories: " + ex.Message, ex);
            }
        }
    }
}