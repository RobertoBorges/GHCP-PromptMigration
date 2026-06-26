// =============================================================================
// REST API Controller Template
// =============================================================================
// Replacement pattern for WCF ServiceContract
// =============================================================================

using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;

namespace MyApp.Api.Controllers;

/// <summary>
/// REST API controller replacing WCF {ServiceName}Service
/// 
/// WCF Migration Notes:
/// - [ServiceContract] → [ApiController]
/// - [OperationContract] → [HttpGet], [HttpPost], etc.
/// - [FaultContract] → Returns ProblemDetails on error
/// - [DataContract] → DTO classes with validation attributes
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(
        IProductService productService,
        ILogger<ProductsController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    // =========================================================================
    // WCF: [OperationContract] Product GetProduct(int id)
    // REST: GET /api/products/{id}
    // =========================================================================
    /// <summary>
    /// Get a product by ID
    /// </summary>
    /// <param name="id">Product identifier</param>
    /// <returns>Product details or NotFound</returns>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        try
        {
            var product = await _productService.GetByIdAsync(id);
            
            if (product is null)
            {
                return NotFound(new ProblemDetails
                {
                    Title = "Product Not Found",
                    Detail = $"Product with ID {id} was not found",
                    Status = StatusCodes.Status404NotFound
                });
            }

            return Ok(product);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving product {ProductId}", id);
            throw; // Let exception middleware handle it
        }
    }

    // =========================================================================
    // WCF: [OperationContract] List<Product> GetAllProducts()
    // REST: GET /api/products
    // =========================================================================
    /// <summary>
    /// Get all products with optional filtering
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<ProductDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetAll(
        [FromQuery] string? category = null,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        var products = await _productService.GetAllAsync(category, page, pageSize);
        return Ok(products);
    }

    // =========================================================================
    // WCF: [OperationContract] void CreateProduct(Product product)
    // REST: POST /api/products
    // =========================================================================
    /// <summary>
    /// Create a new product
    /// </summary>
    [HttpPost]
    [Authorize] // Requires authentication
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<ProductDto>> Create([FromBody] CreateProductRequest request)
    {
        if (!ModelState.IsValid)
        {
            return ValidationProblem(ModelState);
        }

        var product = await _productService.CreateAsync(request);
        
        return CreatedAtAction(
            nameof(GetById),
            new { id = product.Id },
            product);
    }

    // =========================================================================
    // WCF: [OperationContract] void UpdateProduct(Product product)
    // REST: PUT /api/products/{id}
    // =========================================================================
    /// <summary>
    /// Update an existing product
    /// </summary>
    [HttpPut("{id:int}")]
    [Authorize]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ProductDto>> Update(
        int id, 
        [FromBody] UpdateProductRequest request)
    {
        if (id != request.Id)
        {
            return BadRequest(new ProblemDetails
            {
                Title = "ID Mismatch",
                Detail = "Route ID does not match request body ID"
            });
        }

        var product = await _productService.UpdateAsync(request);
        
        if (product is null)
        {
            return NotFound();
        }

        return Ok(product);
    }

    // =========================================================================
    // WCF: [OperationContract] void DeleteProduct(int id)
    // REST: DELETE /api/products/{id}
    // =========================================================================
    /// <summary>
    /// Delete a product
    /// </summary>
    [HttpDelete("{id:int}")]
    [Authorize(Roles = "Admin")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(int id)
    {
        var deleted = await _productService.DeleteAsync(id);
        
        if (!deleted)
        {
            return NotFound();
        }

        return NoContent();
    }
}

// =============================================================================
// DTOs (Replace WCF [DataContract] classes)
// =============================================================================

/// <summary>
/// Product response DTO
/// Replaces: [DataContract] public class Product
/// </summary>
public record ProductDto
{
    public int Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public string? Description { get; init; }
    public decimal Price { get; init; }
    public string Category { get; init; } = string.Empty;
    public bool IsActive { get; init; }
    public DateTime CreatedAt { get; init; }
    public DateTime? UpdatedAt { get; init; }
}

/// <summary>
/// Create product request DTO
/// </summary>
public record CreateProductRequest
{
    [Required]
    [StringLength(200, MinimumLength = 1)]
    public string Name { get; init; } = string.Empty;

    [StringLength(2000)]
    public string? Description { get; init; }

    [Required]
    [Range(0.01, 999999.99)]
    public decimal Price { get; init; }

    [Required]
    public string Category { get; init; } = string.Empty;
}

/// <summary>
/// Update product request DTO
/// </summary>
public record UpdateProductRequest
{
    [Required]
    public int Id { get; init; }

    [Required]
    [StringLength(200, MinimumLength = 1)]
    public string Name { get; init; } = string.Empty;

    [StringLength(2000)]
    public string? Description { get; init; }

    [Required]
    [Range(0.01, 999999.99)]
    public decimal Price { get; init; }

    [Required]
    public string Category { get; init; } = string.Empty;

    public bool IsActive { get; init; } = true;
}

// =============================================================================
// Service Interface (Replaces WCF Service Implementation)
// =============================================================================

public interface IProductService
{
    Task<ProductDto?> GetByIdAsync(int id);
    Task<IEnumerable<ProductDto>> GetAllAsync(string? category, int page, int pageSize);
    Task<ProductDto> CreateAsync(CreateProductRequest request);
    Task<ProductDto?> UpdateAsync(UpdateProductRequest request);
    Task<bool> DeleteAsync(int id);
}
