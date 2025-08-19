using System;
using System.Collections.Generic;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Reflection;
using System.Reflection.Emit;
using BookShop.Common.Models;
using BookShop.DataAccess.Repositories;

// Helper classes to create dynamic objects in .NET 2.0/3.5
public class DynamicObject
{
    public static object CreateDynamicObject(PropertyInfo[] properties)
    {
        TypeBuilder typeBuilder = CreateTypeBuilder("DynamicAssembly", "DynamicModule", "DynamicType" + Guid.NewGuid().ToString().Replace("-", ""));
        foreach (PropertyInfo property in properties)
        {
            CreateProperty(typeBuilder, property.Name, property.PropertyType);
        }
        
        Type type = typeBuilder.CreateType();
        object instance = Activator.CreateInstance(type);
        
        foreach (PropertyInfo property in properties)
        {
            type.GetProperty(property.Name).SetValue(instance, property.GetValue(property.DeclaringType, null), null);
        }
        
        return instance;
    }
    
    private static TypeBuilder CreateTypeBuilder(string assemblyName, string moduleName, string typeName)
    {
        AssemblyName assembly = new AssemblyName(assemblyName);
        AssemblyBuilder assemblyBuilder = AppDomain.CurrentDomain.DefineDynamicAssembly(assembly, AssemblyBuilderAccess.Run);
        ModuleBuilder moduleBuilder = assemblyBuilder.DefineDynamicModule(moduleName);
        TypeBuilder typeBuilder = moduleBuilder.DefineType(typeName, TypeAttributes.Public);
        return typeBuilder;
    }
    
    private static void CreateProperty(TypeBuilder typeBuilder, string propertyName, Type propertyType)
    {
        FieldBuilder fieldBuilder = typeBuilder.DefineField("_" + propertyName.ToLower(), propertyType, FieldAttributes.Private);
        
        PropertyBuilder propertyBuilder = typeBuilder.DefineProperty(propertyName, PropertyAttributes.None, propertyType, null);
        
        MethodAttributes getSetAttributes = MethodAttributes.Public | MethodAttributes.SpecialName | MethodAttributes.HideBySig;
        
        // Define the "get" accessor method
        MethodBuilder getMethodBuilder = typeBuilder.DefineMethod("get_" + propertyName, getSetAttributes, propertyType, Type.EmptyTypes);
        ILGenerator getIL = getMethodBuilder.GetILGenerator();
        getIL.Emit(OpCodes.Ldarg_0);
        getIL.Emit(OpCodes.Ldfld, fieldBuilder);
        getIL.Emit(OpCodes.Ret);
        
        // Define the "set" accessor method
        MethodBuilder setMethodBuilder = typeBuilder.DefineMethod("set_" + propertyName, getSetAttributes, null, new Type[] { propertyType });
        ILGenerator setIL = setMethodBuilder.GetILGenerator();
        setIL.Emit(OpCodes.Ldarg_0);
        setIL.Emit(OpCodes.Ldarg_1);
        setIL.Emit(OpCodes.Stfld, fieldBuilder);
        setIL.Emit(OpCodes.Ret);
        
        propertyBuilder.SetGetMethod(getMethodBuilder);
        propertyBuilder.SetSetMethod(setMethodBuilder);
    }
}

public class DynamicProperty<T>
{
    private string _name;
    private T _value;
    
    public string Name { get { return _name; } }
    public T Value { get { return _value; } }
    
    public DynamicProperty(string name, T value)
    {
        _name = name;
        _value = value;
    }
    
    public PropertyInfo GetPropertyInfo()
    {
        PropertyInfo[] properties = typeof(DynamicProperty<T>).GetProperties();
        PropertyInfo nameProperty = typeof(DynamicProperty<T>).GetProperty("Name");
        PropertyInfo valueProperty = typeof(DynamicProperty<T>).GetProperty("Value");
        
        TypeBuilder typeBuilder = CreateTypeBuilder("DynamicAssemblyProperty", "DynamicModuleProperty", "DynamicPropertyType" + Guid.NewGuid().ToString().Replace("-", ""));
        PropertyBuilder propertyBuilder = typeBuilder.DefineProperty(Name, PropertyAttributes.None, typeof(T), null);
        
        FieldBuilder fieldBuilder = typeBuilder.DefineField("_" + Name.ToLower(), typeof(T), FieldAttributes.Private);
        MethodAttributes getSetAttributes = MethodAttributes.Public | MethodAttributes.SpecialName | MethodAttributes.HideBySig;
        
        // Define the "get" method
        MethodBuilder getMethodBuilder = typeBuilder.DefineMethod("get_" + Name, getSetAttributes, typeof(T), Type.EmptyTypes);
        ILGenerator getIL = getMethodBuilder.GetILGenerator();
        getIL.Emit(OpCodes.Ldarg_0);
        getIL.Emit(OpCodes.Ldfld, fieldBuilder);
        getIL.Emit(OpCodes.Ret);
        
        // Define the "set" method
        MethodBuilder setMethodBuilder = typeBuilder.DefineMethod("set_" + Name, getSetAttributes, null, new Type[] { typeof(T) });
        ILGenerator setIL = setMethodBuilder.GetILGenerator();
        setIL.Emit(OpCodes.Ldarg_0);
        setIL.Emit(OpCodes.Ldarg_1);
        setIL.Emit(OpCodes.Stfld, fieldBuilder);
        setIL.Emit(OpCodes.Ret);
        
        propertyBuilder.SetGetMethod(getMethodBuilder);
        propertyBuilder.SetSetMethod(setMethodBuilder);
        
        Type type = typeBuilder.CreateType();
        object instance = Activator.CreateInstance(type);
        PropertyInfo property = type.GetProperty(Name);
        property.SetValue(instance, Value, null);
        
        return property;
    }
    
    private static TypeBuilder CreateTypeBuilder(string assemblyName, string moduleName, string typeName)
    {
        AssemblyName assembly = new AssemblyName(assemblyName);
        AssemblyBuilder assemblyBuilder = AppDomain.CurrentDomain.DefineDynamicAssembly(assembly, AssemblyBuilderAccess.Run);
        ModuleBuilder moduleBuilder = assemblyBuilder.DefineDynamicModule(moduleName);
        TypeBuilder typeBuilder = moduleBuilder.DefineType(typeName, TypeAttributes.Public);
        return typeBuilder;
    }
}

public partial class Books : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadCategories();
            LoadBooks();
        }
    }

    private void LoadCategories()
    {
        try
        {
            // First add the "All Categories" option
            CategoryDropDown.Items.Add(new ListItem("All Categories", "0"));
            
            try
            {
                // Get categories from database using CategoryRepository
                CategoryRepository categoryRepository = new CategoryRepository();
                List<Category> categories = categoryRepository.GetAllCategories();
                
                // Add each category to dropdown
                foreach (Category category in categories)
                {
                    CategoryDropDown.Items.Add(new ListItem(category.Name, category.CategoryId.ToString()));
                }
            }
            catch (Exception ex)
            {
                // If database access fails, fall back to sample categories
                System.Diagnostics.Debug.WriteLine("Error loading categories from database: " + ex.Message);
                
                // Create sample categories
                List<Category> fallbackCategories = new List<Category>();
                fallbackCategories.Add(CreateCategory(1, "Fiction"));
                fallbackCategories.Add(CreateCategory(2, "Non-Fiction"));
                fallbackCategories.Add(CreateCategory(3, "Science Fiction"));
                fallbackCategories.Add(CreateCategory(4, "Mystery"));
                fallbackCategories.Add(CreateCategory(5, "Romance"));
                
                // Add sample categories to dropdown
                foreach (Category category in fallbackCategories)
                {
                    CategoryDropDown.Items.Add(new ListItem(category.Name, category.CategoryId.ToString()));
                }
                
                // Log the error but don't show it to user for categories
                System.Diagnostics.Debug.WriteLine("Using fallback categories. Error: " + ex.Message);
            }
        }
        catch (Exception ex)
        {
            ShowMessage("Error loading categories: " + ex.Message, false);
        }
    }

    private void LoadBooks()
    {
        try
        {
            List<Book> books;
            int selectedCategoryId = Convert.ToInt32(CategoryDropDown.SelectedValue);
            
            // Create repository instance
            BookRepository bookRepository = new BookRepository();
            
            // If a category is selected, get books for that category directly from the repository
            if (selectedCategoryId > 0)
            {
                books = bookRepository.GetBooksByCategory(selectedCategoryId);
            }
            else
            {
                // Otherwise get all books
                books = bookRepository.GetAllBooks();
            }

            if (books.Count > 0) // Instead of using LINQ Any()
            {
                BooksRepeater.DataSource = books;
                BooksRepeater.DataBind();
                NoResultsLabel.Visible = false;
            }
            else
            {
                BooksRepeater.DataSource = null;
                BooksRepeater.DataBind();
                NoResultsLabel.Visible = true;
            }
        }
        catch (Exception ex)
        {
            ShowMessage("Error loading books: " + ex.Message, false);
        }
    }

    protected void CategoryDropDown_SelectedIndexChanged(object sender, EventArgs e)
    {
        LoadBooks();
    }

    private void ShowMessage(string message, bool isSuccess)
    {
        MessageLabel.Text = message;
        MessageLabel.CssClass = isSuccess ? "message success" : "message error";
        MessageLabel.Visible = true;
    }

    // Helper method to create a category object
    private Category CreateCategory(int id, string name)
    {
        Category category = new Category();
        category.CategoryId = id;
        category.Name = name;
        return category;
    }
    
    // Helper method to create an author object
    private Author CreateAuthor(string fullName)
    {
        Author author = new Author();
        
        // Split fullName into first and last name
        string[] nameParts = fullName.Split(' ');
        if (nameParts.Length > 1)
        {
            author.FirstName = nameParts[0];
            author.LastName = nameParts[nameParts.Length - 1]; // Take last part as last name
        }
        else
        {
            author.FirstName = fullName;
            author.LastName = "";
        }
        
        return author;
    }
    
    // Helper method to create a category with ID and name
    private Category CreateCategoryWithIdName(int categoryId, string name)
    {
        Category category = new Category();
        category.CategoryId = categoryId;
        category.Name = name;
        return category;
    }
        
        // Helper method to create a book object
    private Book CreateBook(int bookId, string title, string authorFullName,
                            int categoryId, string categoryName, decimal price,
                            int stockQuantity, string imageUrl)
    {
        Author author = CreateAuthor(authorFullName);
        Category category = CreateCategoryWithIdName(categoryId, categoryName);

        Book book = new BookShop.Common.Models.Book();
        book.BookId = bookId;
        book.Title = title;
        book.Author = author;
        book.Category = category;
        book.Price = price;
        book.StockQuantity = stockQuantity;
        book.ImageUrl = imageUrl;
        return book;
    }

    private List<Book> GetSampleBooks()
    {
        try
        {
            // Get actual books from the database using BookRepository
            BookRepository bookRepository = new BookRepository();
            List<Book> books = bookRepository.GetAllBooks();
            
            // Return all books from the database
            return books;
        }
        catch (Exception ex)
        {
            // Log the error
            System.Diagnostics.Debug.WriteLine("Error loading books from database: " + ex.Message);
            
            // If there's an error accessing the database, fall back to sample data
            List<Book> fallbackBooks = new List<Book>();
            
            // Create fallback sample data
            fallbackBooks.Add(CreateBook(
                1, 
                "Harry Potter and the Philosopher's Stone", 
                "J.K. Rowling", 
                1, 
                "Fiction", 
                12.99m, 
                50, 
                "~/images/books/harry-potter-1.jpg"
            ));
            
            fallbackBooks.Add(CreateBook(
                2, 
                "The Shining", 
                "Stephen King", 
                4, 
                "Mystery", 
                14.99m, 
                30, 
                "~/images/books/the-shining.jpg"
            ));
            
            // Show the error message
            ShowMessage("Unable to connect to database. Showing sample data instead. Error: " + ex.Message, false);
            
            return fallbackBooks;
        }
    }
}