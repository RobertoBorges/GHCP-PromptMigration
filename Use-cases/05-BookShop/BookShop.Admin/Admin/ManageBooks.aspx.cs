using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Admin_ManageBooks : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadBooks();
            LoadStatistics();
        }
    }

    private void LoadBooks()
    {
        try
        {
            // In a real application, this would use BookService.GetAllBooks()
            var books = GetSampleBooks();
            
            BooksGridView.DataSource = books;
            BooksGridView.DataBind();
        }
        catch (Exception ex)
        {
            ShowMessage("Error loading books: " + ex.Message, false);
        }
    }

    private void LoadStatistics()
    {
        try
        {
            var books = GetSampleBooks();
            
            TotalBooksLabel.Text = books.Count.ToString();
            ActiveBooksLabel.Text = books.Count(b => GetIsActive(b)).ToString();
            LowStockBooksLabel.Text = books.Count(b => GetStockQuantity(b) < 10).ToString();
            OutOfStockBooksLabel.Text = books.Count(b => GetStockQuantity(b) == 0).ToString();
        }
        catch (Exception ex)
        {
            ShowMessage("Error loading statistics: " + ex.Message, false);
        }
    }

    protected void AddNewBookButton_Click(object sender, EventArgs e)
    {
        // In a real application, this would redirect to AddEditBook.aspx
        ShowMessage("Add Book functionality would be implemented here.", true);
    }

    protected void RefreshButton_Click(object sender, EventArgs e)
    {
        LoadBooks();
        LoadStatistics();
        ShowMessage("Book list refreshed successfully.", true);
    }

    protected void BooksGridView_RowCommand(object sender, GridViewCommandEventArgs e)
    {
        if (e.CommandName == "EditBook")
        {
            int bookId = Convert.ToInt32(e.CommandArgument);
            // In a real application, redirect to edit page
            ShowMessage($"Edit Book ID: {bookId} - functionality would be implemented here.", true);
        }
        else if (e.CommandName == "DeleteBook")
        {
            int bookId = Convert.ToInt32(e.CommandArgument);
            // In a real application, call BookService.DeleteBook(bookId)
            ShowMessage($"Book ID: {bookId} would be deleted from inventory.", true);
            LoadBooks();
            LoadStatistics();
        }
    }

    protected void BooksGridView_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
            // Color code rows based on stock levels
            int stockQuantity = GetStockQuantity(e.Row.DataItem);
            
            if (stockQuantity == 0)
            {
                e.Row.BackColor = System.Drawing.Color.FromArgb(255, 182, 193); // Light red
            }
            else if (stockQuantity < 10)
            {
                e.Row.BackColor = System.Drawing.Color.FromArgb(255, 255, 224); // Light yellow
            }
        }
    }

    private void ShowMessage(string message, bool isSuccess)
    {
        MessageLabel.Text = message;
        MessageLabel.CssClass = isSuccess ? "message success" : "message error";
        MessageLabel.Visible = true;
    }

    private int GetStockQuantity(object book)
    {
        return Convert.ToInt32(book.GetType().GetProperty("StockQuantity").GetValue(book, null));
    }

    private bool GetIsActive(object book)
    {
        return Convert.ToBoolean(book.GetType().GetProperty("IsActive").GetValue(book, null));
    }

    private List<object> GetSampleBooks()
    {
        return new List<object>
        {
            new {
                BookId = 1,
                Title = "Harry Potter and the Philosopher's Stone",
                Author = new { FullName = "J.K. Rowling" },
                Category = new { Name = "Fiction" },
                ISBN = "978-0747532699",
                Price = 12.99m,
                StockQuantity = 50,
                IsActive = true
            },
            new {
                BookId = 2,
                Title = "The Shining",
                Author = new { FullName = "Stephen King" },
                Category = new { Name = "Horror" },
                ISBN = "978-0307743657",
                Price = 14.99m,
                StockQuantity = 5,
                IsActive = true
            },
            new {
                BookId = 3,
                Title = "Out of Print Book",
                Author = new { FullName = "Unknown Author" },
                Category = new { Name = "Fiction" },
                ISBN = "978-0000000000",
                Price = 19.99m,
                StockQuantity = 0,
                IsActive = false
            },
            new {
                BookId = 4,
                Title = "Foundation",
                Author = new { FullName = "Isaac Asimov" },
                Category = new { Name = "Science Fiction" },
                ISBN = "978-0553293357",
                Price = 15.99m,
                StockQuantity = 20,
                IsActive = true
            },
            new {
                BookId = 5,
                Title = "Low Stock Book",
                Author = new { FullName = "Test Author" },
                Category = new { Name = "Mystery" },
                ISBN = "978-1111111111",
                Price = 10.99m,
                StockQuantity = 3,
                IsActive = true
            }
        };
    }
}