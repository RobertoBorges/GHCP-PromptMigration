using FluentAssertions;
using Moq;
using Xunit;

namespace MyApp.Tests;

/// <summary>
/// Base class for unit tests with common setup patterns
/// </summary>
public abstract class UnitTestBase
{
    protected readonly Mock<ILogger<T>> CreateLoggerMock<T>() => new();
    
    protected readonly DateTimeOffset FixedNow = new(2024, 1, 15, 10, 30, 0, TimeSpan.Zero);
}

/// <summary>
/// Example: Testing a migrated service
/// Demonstrates patterns for validating business logic preserved during migration
/// </summary>
public class ProductServiceTests : UnitTestBase
{
    private readonly Mock<IProductRepository> _repositoryMock;
    private readonly Mock<ICacheService> _cacheMock;
    private readonly ProductService _sut;

    public ProductServiceTests()
    {
        _repositoryMock = new Mock<IProductRepository>();
        _cacheMock = new Mock<ICacheService>();
        _sut = new ProductService(_repositoryMock.Object, _cacheMock.Object);
    }

    [Fact]
    public async Task GetByIdAsync_WhenProductExists_ReturnsProduct()
    {
        // Arrange
        var productId = 1;
        var expected = new Product { Id = productId, Name = "Test Product", Price = 9.99m };
        _repositoryMock.Setup(r => r.GetByIdAsync(productId))
            .ReturnsAsync(expected);

        // Act
        var result = await _sut.GetByIdAsync(productId);

        // Assert
        result.Should().NotBeNull();
        result.Should().BeEquivalentTo(expected);
    }

    [Fact]
    public async Task GetByIdAsync_WhenProductNotFound_ReturnsNull()
    {
        // Arrange
        _repositoryMock.Setup(r => r.GetByIdAsync(It.IsAny<int>()))
            .ReturnsAsync((Product?)null);

        // Act
        var result = await _sut.GetByIdAsync(999);

        // Assert
        result.Should().BeNull();
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public async Task GetByIdAsync_WithInvalidId_ThrowsArgumentException(int invalidId)
    {
        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(() => _sut.GetByIdAsync(invalidId));
    }

    [Fact]
    public async Task GetAllAsync_ReturnsAllProducts()
    {
        // Arrange
        var products = new List<Product>
        {
            new() { Id = 1, Name = "Product 1", Price = 10.00m },
            new() { Id = 2, Name = "Product 2", Price = 20.00m }
        };
        _repositoryMock.Setup(r => r.GetAllAsync()).ReturnsAsync(products);

        // Act
        var result = await _sut.GetAllAsync();

        // Assert
        result.Should().HaveCount(2);
        result.Should().BeEquivalentTo(products);
    }

    [Fact]
    public async Task CreateAsync_ValidProduct_ReturnsCreatedProduct()
    {
        // Arrange
        var newProduct = new Product { Name = "New Product", Price = 15.99m };
        _repositoryMock.Setup(r => r.AddAsync(It.IsAny<Product>()))
            .ReturnsAsync((Product p) => { p.Id = 1; return p; });

        // Act
        var result = await _sut.CreateAsync(newProduct);

        // Assert
        result.Should().NotBeNull();
        result.Id.Should().Be(1);
        _repositoryMock.Verify(r => r.AddAsync(It.Is<Product>(p => p.Name == "New Product")), Times.Once);
    }

    [Fact]
    public async Task UpdateAsync_ExistingProduct_UpdatesSuccessfully()
    {
        // Arrange
        var product = new Product { Id = 1, Name = "Updated Name", Price = 25.00m };
        _repositoryMock.Setup(r => r.ExistsAsync(1)).ReturnsAsync(true);
        _repositoryMock.Setup(r => r.UpdateAsync(It.IsAny<Product>())).Returns(Task.CompletedTask);

        // Act
        await _sut.UpdateAsync(product);

        // Assert
        _repositoryMock.Verify(r => r.UpdateAsync(It.Is<Product>(p => p.Id == 1)), Times.Once);
    }
}

// =============================================================================
// Sample interfaces/classes for the tests above (would be in actual project)
// =============================================================================

public interface IProductRepository
{
    Task<Product?> GetByIdAsync(int id);
    Task<List<Product>> GetAllAsync();
    Task<Product> AddAsync(Product product);
    Task UpdateAsync(Product product);
    Task<bool> ExistsAsync(int id);
}

public interface ICacheService
{
    Task<T?> GetAsync<T>(string key);
    Task SetAsync<T>(string key, T value, TimeSpan? expiry = null);
}

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
}

public class ProductService
{
    private readonly IProductRepository _repository;
    private readonly ICacheService _cache;

    public ProductService(IProductRepository repository, ICacheService cache)
    {
        _repository = repository;
        _cache = cache;
    }

    public async Task<Product?> GetByIdAsync(int id)
    {
        if (id <= 0) throw new ArgumentException("Invalid product ID", nameof(id));
        return await _repository.GetByIdAsync(id);
    }

    public async Task<List<Product>> GetAllAsync() => await _repository.GetAllAsync();

    public async Task<Product> CreateAsync(Product product) => await _repository.AddAsync(product);

    public async Task UpdateAsync(Product product)
    {
        if (!await _repository.ExistsAsync(product.Id))
            throw new InvalidOperationException("Product not found");
        await _repository.UpdateAsync(product);
    }
}
