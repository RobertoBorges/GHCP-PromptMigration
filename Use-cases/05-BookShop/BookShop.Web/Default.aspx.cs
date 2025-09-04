using System;
using System.Collections.Generic;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.IO;
using BookShop.Common.Models;

public partial class _Default : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadFeaturedBooks();
        }
    }

    private void LoadFeaturedBooks()
    {
        try
        {
            // In a real application, we would use the BookService here
            // For now, create some sample data for demonstration
            List<Book> featuredBooks = CreateSampleBooks();
            // Get first 4 books using standard collection indexing (compatible with .NET 3.5)
            List<object> firstFourBooks = new List<object>();
            int count = 0;
            foreach (object book in featuredBooks)
            {
                if (count < 4)
                {
                    firstFourBooks.Add(book);
                    count++;
                }
                else
                {
                    break;
                }
            }
            FeaturedBooksRepeater.DataSource = firstFourBooks; // Show first 4 books
            FeaturedBooksRepeater.DataBind();
        }
        catch (Exception ex)
        {
            // Log error and show user-friendly message
            Response.Write("<div class='message error'>Error loading featured books: " + ex.Message + "</div>");
        }
    }

    private List<Book> CreateSampleBooks()
    {
        // Sample data for demonstration - in real app this would come from BookService
        List<Book> books = new List<Book>();
        
        // Book 1
        Book book1 = new Book();
        book1.BookId = 1;
        book1.Title = "Harry Potter and the Philosopher's Stone";
        Author author1 = new Author();
        author1.FirstName = "J.K.";
        author1.LastName = "Rowling";
        book1.Author = author1;
        Category category1 = new Category();
        category1.Name = "Fiction";
        book1.Category = category1;
        book1.Price = 12.99m;
        book1.ImageUrl = "~/images/books/harry-potter-1.jpg";
        books.Add(book1);
        
        // Book 2
        Book book2 = new Book();
        book2.BookId = 2;
        book2.Title = "The Shining";
        Author author2 = new Author();
        author2.FirstName = "Stephen";
        author2.LastName = "King";
        book2.Author = author2;
        Category category2 = new Category();
        category2.Name = "Horror";
        book2.Category = category2;
        book2.Price = 14.99m;
        book2.ImageUrl = "~/images/books/the-shining.jpg";
        books.Add(book2);
        
        // Book 3
        Book book3 = new Book();
        book3.BookId = 3;
        book3.Title = "Pride and Prejudice";
        Author author3 = new Author();
        author3.FirstName = "Jane";
        author3.LastName = "Austen";
        book3.Author = author3;
        Category category3 = new Category();
        category3.Name = "Romance";
        book3.Category = category3;
        book3.Price = 11.99m;
        book3.ImageUrl = "~/images/books/pride-prejudice.jpg";
        books.Add(book3);
        
        // Book 4
        Book book4 = new Book();
        book4.BookId = 4;
        book4.Title = "1984";
        Author author4 = new Author();
        author4.FirstName = "George";
        author4.LastName = "Orwell";
        book4.Author = author4;
        Category category4 = new Category();
        category4.Name = "Fiction";
        book4.Category = category4;
        book4.Price = 13.99m;
        book4.ImageUrl = "~/images/books/1984.jpg";
        books.Add(book4);
        
        return books;
    }
}