# WebForms to Razor Pages / Blazor

Use this skill when migrating ASP.NET Web Forms (`.aspx`, `.ascx`, `.master`) to a modern .NET 8 UI stack.

## When to use

Apply this skill when the source uses server controls, code-behind, ViewState, postbacks, `UpdatePanel`, `GridView`, or `LoginView`.

## Target selection

- Prefer **Razor Pages** for page-centric forms, CRUD flows, and straightforward request/response UX.
- Prefer **Blazor Server/Web App** only when the legacy app relies heavily on rich server-driven interactivity.
- Use **MVC controllers + Razor views** when the app already has controller-style composition needs.

## Mapping guide

| Web Forms concept | Modern target |
|---|---|
| `.master` page | shared layout `_Layout.cshtml` |
| code-behind events | page handlers, controllers, or component callbacks |
| `GridView` | Razor table + partial/component |
| `Repeater` | `@foreach` over a view model |
| `UpdatePanel` | full-page post/redirect/get, HTMX-style partial updates, or Blazor component interaction |
| ViewState | explicit model binding and persisted state |
| `Session` | distributed cache/session only when truly required |

## Migration approach

1. Split UI, business logic, and data access before rewriting screens.
2. Create page/view models rather than porting code-behind classes line-for-line.
3. Replace implicit server control behavior with explicit HTML, tag helpers, and validation.
4. Rebuild authentication using ASP.NET Core identity or Entra ID.
5. Preserve routes, page purpose, and user-visible workflows whenever possible.

## Example target pattern

```csharp
public class BooksModel(IBookService books) : PageModel
{
    public IReadOnlyList<BookDto> Items { get; private set; } = [];

    public async Task OnGetAsync(CancellationToken cancellationToken)
    {
        Items = await books.ListAsync(cancellationToken);
    }
}
```

```html
@page
@model BooksModel
<table class="table">
  @foreach (var book in Model.Items)
  {
    <tr><td>@book.Title</td><td>@book.Price</td></tr>
  }
</table>
```

## Validation checklist

- Required pages and navigation still exist.
- Form validation and anti-forgery are implemented explicitly.
- No business logic remains trapped in page markup.
- Uploaded files, auth flows, and session-dependent behavior are accounted for.
