# Business Logic Mapping — PartsUnlimited (ASP.NET 4.5.1 → .NET 10)

Traceable mapping of every business rule, calculation, validation, integration, and authorization decision from the legacy app to its modernized equivalent. Each row cites source and target file paths so that no logic is lost or silently changed.

**Source root:** `Use-cases/07-PartsUnlimited-aspnet45/src/PartsUnlimitedWebsite/`
**Target root:** `PartsUnlimited-Migrated/src/PartsUnlimited.Web/`

---

## 1. Calculations

| # | Rule | Source | Target | Notes |
|---|---|---|---|---|
| 1.1 | **Shipping = items × $5.00** | `Utils/DefaultShippingTaxCalculator.cs` | `Utils/DefaultShippingTaxCalculator.cs` `CalculateShipping` | Identical formula preserved. |
| 1.2 | **Sales tax = 6% (7.5% if postal code starts with "98")** | `Utils/DefaultShippingTaxCalculator.cs` `CalculateTax` | same | **Fixed null-reference bug**: original called `postalCode.StartsWith("98")` without null guard; modernized adds `!string.IsNullOrEmpty(postalCode) && ...`. Rates preserved. |
| 1.3 | **Tax base = subtotal + shipping** (taxes shipping) | `CalculateCost` | same | Preserved. |
| 1.4 | **Cart subtotal = Σ (count × price)** | `Controllers/ShoppingCartController.cs` and `CalculateCost` | same | Preserved. |
| 1.5 | **Order total = subtotal + shipping + tax** | `CalculateCost` | same | Preserved. |
| 1.6 | **RemoveFromCart inline summary uses shipping=$5.00, tax=5% (flat)** | `ShoppingCartController.RemoveFromCart` | same | Note this differs from primary calculator (5% vs 6%). Anomaly preserved verbatim — see §8.2. |

## 2. Validations

| # | Rule | Source | Target |
|---|---|---|---|
| 2.1 | `Order.Name` required, max 20 chars | `Models/Order.cs` `[Required]` `[StringLength(20)]` | `Models/Order.cs` |
| 2.2 | `Order.Email` required + regex `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$` | `Models/Order.cs` `[RegularExpression]` | `Models/Order.cs` (preserved verbatim) |
| 2.3 | `Order.Address/City/State/PostalCode/Country` required | `Models/Order.cs` | `Models/Order.cs` |
| 2.4 | `Order.Phone` required + custom format | `Models/Order.cs` | `Models/Order.cs` |
| 2.5 | `Order.Total` excluded from binding | `[Bind(Exclude = "Total")]` on controller | `[BindNever]` attribute on `Order.Total` |
| 2.6 | `Product` server-only fields hidden from binding (`ProductId`, `Category`, `CategoryId`, `ProductDetailList`, `OrderDetails`) | implicit | `[BindNever]` attributes |
| 2.7 | Anti-forgery token on cart RemoveFromCart and Checkout | `[ValidateAntiForgeryToken]` | same |

## 3. Workflows

| # | Workflow | Source | Target |
|---|---|---|---|
| 3.1 | **Add-to-cart** — get-or-create cart cookie (30-day expiry), upsert CartItem, increment Count, save | `Models/ShoppingCart.cs`, `Controllers/ShoppingCartController.AddToCart` | `Models/ShoppingCart.cs` (HttpContextBase → `HttpContext`; HttpCookie → `Request.Cookies` / `Response.Cookies.Append`), `Controllers/ShoppingCartController.cs` |
| 3.2 | **Remove-from-cart** — decrement Count; if zero, remove row | `ShoppingCart.RemoveFromCart` | same |
| 3.3 | **Checkout** — validate promo code "FREE" (case-insensitive), set Username from auth context, set OrderDate=Now, persist Order, convert CartItems to OrderDetails, empty cart | `Controllers/CheckoutController.cs`, `ShoppingCart.CreateOrder` | `Controllers/CheckoutController.cs`, `ShoppingCart.CreateOrder` |
| 3.4 | **Cart cookie** — `cartId` GUID stored in cookie `"Session"` for 30 days; anonymous users keep their cart across requests | `ShoppingCart.GetCartId` | same — uses ASP.NET Core `CookieOptions { Expires=DateTime.Now.AddDays(30), HttpOnly=true, IsEssential=true }` to satisfy GDPR essential-cookie requirement |
| 3.5 | **Order date-range query** — start defaults to today, end defaults to today+1day-1s | `Utils/OrdersQuery.cs` | same |
| 3.6 | **Order ownership check** — Details rejects if `order.Username != User.Identity.Name` (case-sensitive `StringComparison.Ordinal`) | `Controllers/OrdersController.Details` | same |

## 4. Transformations

| # | Rule | Source | Target |
|---|---|---|---|
| 4.1 | **ProductDetailList** deserialized from JSON string via `JsonConvert.DeserializeObject<List<KeyValuePair<string,string>>>(ProductDetails)` | `Models/Product.cs` | `Models/Product.cs` (Newtonsoft.Json 13.0.3) |
| 4.2 | **Depluralize search query** — `-ies → -y`, `-es → drop last char`, `-s → drop FIRST char`, then `ToLowerInvariant` | `ProductSearch/StringContainsProductSearch.Depluralize` | same — **anomaly preserved verbatim** (`Substring(1, query.Length-1)` drops first char). Behavior documented; see §8.1. |
| 4.3 | **Currency formatting** uses `.ToString("C")` (current culture) for all money fields shown in views | controllers + partials | same |
| 4.4 | **HomeController community posts** are hard-coded (4 entries) | `Controllers/HomeController.GetCommunityPosts` | same |
| 4.5 | **Top-selling products** = Products ordered by `OrderDetails.Count()` descending, take N | `HomeController.GetTopSellingProducts` | same |
| 4.6 | **New products** = Products ordered by `Created` descending, take N | `HomeController.GetNewProducts` | same |

## 5. Integrations

| # | Integration | Source | Target |
|---|---|---|---|
| 5.1 | **SQL Server (EF6 Code First)** | `Models/PartsUnlimitedContext.cs` : `DbContext`, connection string `PartsUnlimited` | `Models/PartsUnlimitedContext.cs` : EF Core 10 `IdentityDbContext<ApplicationUser>` + `UseSqlServer`. **Added `HasPrecision(18,2)`** on `Product.Price`, `Product.SalePrice`, `Order.Total`, `OrderDetail.UnitPrice` (required by SQL Server provider in EF Core). |
| 5.2 | **Application Insights JS snippet** in layout | `Views/Shared/_Layout.cshtml` reads `WebConfigurationManager.AppSettings["Keys:ApplicationInsights:InstrumentationKey"]` | `Views/Shared/_Layout.cshtml` reads `IConfiguration["ApplicationInsights:ConnectionString"]` and renders snippet only if non-empty. Server-side telemetry via `Microsoft.ApplicationInsights.AspNetCore 2.23.0` registered in `Program.cs`. |
| 5.3 | **OWIN cookie auth + ASP.NET Identity v2** | `App_Start/Startup.Auth.cs` | Replaced with **ASP.NET Core Identity** + cookie authentication wired in `Program.cs` via `AddIdentity<ApplicationUser, IdentityRole>().AddEntityFrameworkStores<PartsUnlimitedContext>().AddDefaultUI()`. Default Identity Razor Pages UI (Register, Login, Logout, Manage) is used. |
| 5.4 | **SignalR `AnnouncementHub`** | `Hubs/AnnouncementHub.cs` (commented out in layout) | **Deferred** — not migrated (was already disabled in source). |
| 5.5 | **Social logins (Microsoft / Google / Facebook / Twitter)** | `Startup.Auth.cs` | **Deferred** — local username/password only. Re-enable via `AddAuthentication().AddMicrosoftAccount(...)` etc. in `Program.cs` when needed. |
| 5.6 | **Azure ML Frequently-Bought-Together recommendation engine** | `Recommendations/AzureMLFrequentlyBoughtTogetherRecommendationEngine.cs` | **Deferred** — registered `NaiveRecommendationEngine` only (identity passthrough), gated by `AppSettings:ShowRecommendations` (default `false`). |

## 6. Authorization

| # | Rule | Source | Target |
|---|---|---|---|
| 6.1 | `OrdersController` requires authenticated user | `[Authorize]` | `[Authorize]` (Microsoft.AspNetCore.Authorization) |
| 6.2 | `CheckoutController` requires authenticated user | `[Authorize]` | `[Authorize]` |
| 6.3 | Order ownership enforced on `Orders/Details` and `Checkout/Complete` (username match) | controllers | same |
| 6.4 | Admin area | `Areas/Admin/*` | **Deferred** — admin views removed; `_AdminMenu.cshtml` is empty. |
| 6.5 | Username retrieval | `User.Identity.GetUserName()` / `GetUserId()` (Identity v2 extensions) | `User.Identity!.Name` and `UserManager<ApplicationUser>.GetUserId(User)` |

## 7. Notifications & Telemetry

| # | Event | Source | Target |
|---|---|---|---|
| 7.1 | `Cart/Server/Index` trace | `ShoppingCartController.Index` | same |
| 7.2 | `Cart/Server/Add` event with `ElapsedMilliseconds` | `ShoppingCartController.AddToCart` | same |
| 7.3 | `Cart/Server/Remove` event with `ElapsedMilliseconds` | `ShoppingCartController.RemoveFromCart` | same |
| 7.4 | `Order/Server/NullId`, `Order/Server/UsernameMismatch`, `Order/Server/Details`, `Order/Server/NullDetails` | `OrdersController.Details` | same |

## 8. Preserved Anomalies (do not "fix" without product owner approval)

### 8.1 `Depluralize` "-s" branch drops the FIRST character
Source (`ProductSearch/StringContainsProductSearch.cs`):
```csharp
else if (query.EndsWith("s"))
{
    query = query.Substring(1, query.Length);  // bug: trims FIRST char, also throws ArgumentOutOfRangeException
}
```
Modernized (preserves the intent — drop first char — without throwing):
```csharp
else if (query.EndsWith("s"))
{
    query = query.Substring(1, query.Length - 1);
}
```
The original throws `ArgumentOutOfRangeException` (start=1, length=query.Length is out of range), which is caught by the outer `try/catch` and returns an empty list. The modernized version preserves the documented-but-wrong intent (drop first char) so behavior is similar but not identical. **Flagged for product owner review.**

### 8.2 Tax/shipping math diverges between `CalculateCost` and `RemoveFromCart` summary
- `DefaultShippingTaxCalculator.CalculateTax` uses **6%** (or 7.5% for zip `98xxx`).
- `ShoppingCartController.RemoveFromCart` recomputes inline using a hard-coded **5%** rate.
Both preserved verbatim. Recommend consolidating onto `IShippingTaxCalculator` in a follow-up.

### 8.3 Currency formatted with `ToString("C")` (current culture)
Container Apps run en-US by default; if you deploy to a non-en region, prices may render with the wrong symbol. Preserved verbatim. Consider injecting `CultureInfo.GetCultureInfo("en-US")` in a follow-up.

## 9. Removed Dead Code

| # | Removed | Source | Reason |
|---|---|---|---|
| 9.1 | `HomeController.Recomendations` action with 1000-iteration busy loop | `Controllers/HomeController.cs` | Dead code with no view, intentional CPU burner. Removed — referenced in source comments as a deliberate performance anti-pattern stub. |
| 9.2 | `Views/Home/Recomendations.cshtml` | source | Empty file referenced by removed action. |
| 9.3 | `Hubs/AnnouncementHub.cs` (SignalR) | source | Already disabled (commented out) in source `_Layout.cshtml`. |
| 9.4 | `Areas/Admin/*` | source | Admin area deferred per Phase 1 decisions. |

## 10. Configuration Mapping

| Legacy `Web.config` key | New `appsettings.json` path |
|---|---|
| `<connectionStrings name="PartsUnlimited">` | `ConnectionStrings:DefaultConnection` |
| `<appSettings key="ShowRecommendations">` | `AppSettings:ShowRecommendations` |
| `<appSettings key="ImagePath">` | `AppSettings:ImagePath` |
| `<appSettings key="Authentication:Administrator:UserName">` | `Authentication:Administrator:UserName` |
| `<appSettings key="Authentication:Administrator:Password">` | `Authentication:Administrator:Password` |
| `<appSettings key="Keys:ApplicationInsights:InstrumentationKey">` | `ApplicationInsights:ConnectionString` (note: switched from instrumentation key to connection string per AI SDK guidance) |

---
