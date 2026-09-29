# Web Forms to Razor Migration

Use this skill when migrating ASP.NET Web Forms (`.aspx`, `.ascx`, `.master`) to .NET 8 with Razor Pages, MVC views, or view components.

## When to Use

Apply this skill when the source contains:

- `.aspx`, `.ascx`, `.master`, or `App_Code`
- code-behind event handlers such as `Page_Load`, `btnSave_Click`, or `RowCommand`
- `ViewState`, `UpdatePanel`, `GridView`, `Repeater`, or `LoginView`
- server controls such as `asp:TextBox`, `asp:Button`, `asp:DropDownList`, `asp:UserControl`

## Target Selection

- Prefer **Razor Pages** for page-centric forms and CRUD screens.
- Prefer **MVC + Razor views** when controller composition and richer route orchestration already exist.
- Use **View Components** for reusable UI widgets that replace user controls.
- Use **partial views** for simple reusable markup fragments.

## Mapping Guide

| Web Forms Concept | Modern Target |
|---|---|
| `.aspx` page | `.cshtml` page or MVC view |
| code-behind class | `PageModel`, controller action, or service class |
| `ViewState` | explicit model binding, TempData, Session, hidden fields, or client-side state |
| server controls | HTML + Tag Helpers + model binding |
| `.master` page | `_Layout.cshtml` |
| `.ascx` user control | partial view or View Component |
| postback event | standard form POST, AJAX/fetch, HTMX, or component callback |
| `UpdatePanel` | AJAX endpoint, partial refresh, or Blazor/HTMX-style interaction |

## `.aspx` to `.cshtml` Page Mapping

### Before - Web Forms page

```aspx
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Books.aspx.cs" Inherits="Legacy.Books" %>
<form id="form1" runat="server">
    <asp:GridView ID="BooksGrid" runat="server" AutoGenerateColumns="false">
        <Columns>
            <asp:BoundField DataField="Title" HeaderText="Title" />
            <asp:BoundField DataField="Price" HeaderText="Price" />
        </Columns>
    </asp:GridView>
</form>
```

### After - Razor Page

```html
@page
@model BooksModel

<table class="table">
    <thead>
        <tr><th>Title</th><th>Price</th></tr>
    </thead>
    <tbody>
    @foreach (var book in Model.Items)
    {
        <tr>
            <td>@book.Title</td>
            <td>@book.Price</td>
        </tr>
    }
    </tbody>
</table>
```

## Code-Behind to PageModel Example

### Before - code-behind

```csharp
public partial class Books : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            BooksGrid.DataSource = BookRepository.GetAll();
            BooksGrid.DataBind();
        }
    }
}
```

### After - `PageModel`

```csharp
public sealed class BooksModel(IBookService bookService) : PageModel
{
    public IReadOnlyList<BookDto> Items { get; private set; } = [];

    public async Task OnGetAsync(CancellationToken cancellationToken)
    {
        Items = await bookService.ListAsync(cancellationToken);
    }
}
```

## ViewState Replacement Options

Use the smallest persistence mechanism that preserves the workflow.

| Legacy Need | Replacement |
|---|---|
| One-request flash message | `TempData` |
| Multi-step wizard state | Session or persisted draft entity |
| Simple form state | Model binding + redisplay validation errors |
| Client-side UI state | Hidden fields or JavaScript state |

Avoid re-creating giant ViewState blobs.

## Server Controls to Tag Helpers

### Before

```aspx
<asp:TextBox ID="TitleTextBox" runat="server" />
<asp:Button ID="SaveButton" runat="server" Text="Save" OnClick="SaveButton_Click" />
```

### After

```html
<form method="post">
    <input asp-for="Input.Title" class="form-control" />
    <button type="submit" class="btn btn-primary">Save</button>
</form>
```

```csharp
public sealed class EditBookModel(IBookService bookService) : PageModel
{
    [BindProperty]
    public EditBookInput Input { get; set; } = new();

    public async Task<IActionResult> OnPostAsync(CancellationToken cancellationToken)
    {
        if (!ModelState.IsValid) return Page();
        await bookService.SaveAsync(Input, cancellationToken);
        TempData["SuccessMessage"] = "Book saved.";
        return RedirectToPage("/Books");
    }
}
```

## Master Pages to Layouts

### Before

```aspx
<%@ Master Language="C#" %>
<html>
<body>
    <asp:ContentPlaceHolder ID="MainContent" runat="server" />
</body>
</html>
```

### After

```html
<!DOCTYPE html>
<html>
<head>
    <title>@ViewData["Title"]</title>
</head>
<body>
    <main class="container">
        @RenderBody()
    </main>
</body>
</html>
```

## User Controls to Partial Views / View Components

### Before - `.ascx`

```aspx
<%@ Control Language="C#" %>
<div><%= CurrentUserName %></div>
```

### After - View Component

```csharp
public sealed class CurrentUserViewComponent : ViewComponent
{
    public IViewComponentResult Invoke(string userName) => View(model: userName);
}
```

```html
@await Component.InvokeAsync("CurrentUser", new { userName = User.Identity?.Name ?? "Guest" })
```

## Postback to Form POST / AJAX

### Before

```csharp
protected void SaveButton_Click(object sender, EventArgs e)
{
    Save();
}
```

### After

- Standard form POST for page-oriented workflows
- AJAX/fetch for partial updates
- JSON endpoints for dynamic widgets

## Validation and Security Defaults

- Use model validation attributes instead of implicit control validation only.
- Use antiforgery tokens for form posts.
- Preserve routes and user-visible workflows when possible.
- Move business logic into services, not markup or PageModels.

## Validation Checklist

- Required pages, navigation, and forms still exist.
- Validation, antiforgery, and auth flows are explicit.
- Session-dependent behaviors are intentionally preserved or removed.
- File uploads, paging, sorting, and partial updates have a modern equivalent.

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- Map each major `.aspx` page to a Razor target
- Convert code-behind patterns into `PageModel` or controller actions
- Explain how ViewState and postbacks are replaced
- Call out reusable user control conversion points
