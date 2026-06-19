package com.example.tests;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Unit test examples for migrated Java services
 * Uses JUnit 5, Mockito, and AssertJ
 */
@ExtendWith(MockitoExtension.class)
class ProductServiceTests {

    @Mock
    private ProductRepository repository;

    @Mock
    private CacheService cacheService;

    private ProductService sut;

    @BeforeEach
    void setUp() {
        sut = new ProductService(repository, cacheService);
    }

    @Test
    @DisplayName("getById - when product exists - returns product")
    void getById_WhenProductExists_ReturnsProduct() {
        // Arrange
        var productId = 1L;
        var expected = new Product(productId, "Test Product", 9.99);
        when(repository.findById(productId)).thenReturn(Optional.of(expected));

        // Act
        var result = sut.getById(productId);

        // Assert
        assertThat(result).isPresent();
        assertThat(result.get()).isEqualTo(expected);
    }

    @Test
    @DisplayName("getById - when product not found - returns empty")
    void getById_WhenNotFound_ReturnsEmpty() {
        // Arrange
        when(repository.findById(any())).thenReturn(Optional.empty());

        // Act
        var result = sut.getById(999L);

        // Assert
        assertThat(result).isEmpty();
    }

    @Test
    @DisplayName("getById - with invalid id - throws exception")
    void getById_WithInvalidId_ThrowsException() {
        // Act & Assert
        assertThatThrownBy(() -> sut.getById(0L))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Invalid product ID");
    }

    @Test
    @DisplayName("getAll - returns all products")
    void getAll_ReturnsAllProducts() {
        // Arrange
        var products = List.of(
                new Product(1L, "Product 1", 10.00),
                new Product(2L, "Product 2", 20.00)
        );
        when(repository.findAll()).thenReturn(products);

        // Act
        var result = sut.getAll();

        // Assert
        assertThat(result).hasSize(2);
        assertThat(result).containsExactlyElementsOf(products);
    }

    @Test
    @DisplayName("create - valid product - returns created product")
    void create_ValidProduct_ReturnsCreated() {
        // Arrange
        var newProduct = new Product(null, "New Product", 15.99);
        var savedProduct = new Product(1L, "New Product", 15.99);
        when(repository.save(any(Product.class))).thenReturn(savedProduct);

        // Act
        var result = sut.create(newProduct);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        verify(repository, times(1)).save(any(Product.class));
    }

    @Nested
    @DisplayName("Update operations")
    class UpdateTests {

        @Test
        @DisplayName("update - existing product - updates successfully")
        void update_ExistingProduct_UpdatesSuccessfully() {
            // Arrange
            var product = new Product(1L, "Updated Name", 25.00);
            when(repository.existsById(1L)).thenReturn(true);
            when(repository.save(product)).thenReturn(product);

            // Act
            var result = sut.update(product);

            // Assert
            assertThat(result).isEqualTo(product);
            verify(repository).save(product);
        }

        @Test
        @DisplayName("update - non-existing product - throws exception")
        void update_NonExistingProduct_ThrowsException() {
            // Arrange
            var product = new Product(999L, "Test", 10.00);
            when(repository.existsById(999L)).thenReturn(false);

            // Act & Assert
            assertThatThrownBy(() -> sut.update(product))
                    .isInstanceOf(EntityNotFoundException.class);
        }
    }
}

/**
 * Integration test examples for REST controllers
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class ProductControllerIntegrationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ProductRepository repository;

    @BeforeEach
    void setUp() {
        repository.deleteAll();
    }

    @Test
    @DisplayName("GET /api/products - returns all products")
    void getAllProducts_ReturnsProducts() throws Exception {
        // Arrange
        repository.save(new Product(null, "Product 1", 10.00));
        repository.save(new Product(null, "Product 2", 20.00));

        // Act & Assert
        mockMvc.perform(get("/api/products")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$[0].name").value("Product 1"));
    }

    @Test
    @DisplayName("GET /api/products/{id} - when exists - returns product")
    void getProductById_WhenExists_ReturnsProduct() throws Exception {
        // Arrange
        var product = repository.save(new Product(null, "Test Product", 15.99));

        // Act & Assert
        mockMvc.perform(get("/api/products/{id}", product.getId())
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Test Product"))
                .andExpect(jsonPath("$.price").value(15.99));
    }

    @Test
    @DisplayName("GET /api/products/{id} - when not found - returns 404")
    void getProductById_WhenNotFound_Returns404() throws Exception {
        mockMvc.perform(get("/api/products/{id}", 999)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("POST /api/products - creates new product")
    void createProduct_ValidData_ReturnsCreated() throws Exception {
        // Arrange
        var json = """
                {
                    "name": "New Product",
                    "price": 25.50
                }
                """;

        // Act & Assert
        mockMvc.perform(post("/api/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").exists())
                .andExpect(jsonPath("$.name").value("New Product"));

        assertThat(repository.count()).isEqualTo(1);
    }
}

// =============================================================================
// Sample classes for compilation (would be in actual project)
// =============================================================================

record Product(Long id, String name, double price) {
    public Long getId() { return id; }
}

interface ProductRepository {
    Optional<Product> findById(Long id);
    List<Product> findAll();
    Product save(Product product);
    boolean existsById(Long id);
    void deleteAll();
    long count();
}

interface CacheService {
    <T> Optional<T> get(String key, Class<T> type);
    void set(String key, Object value);
}

class ProductService {
    private final ProductRepository repository;
    private final CacheService cacheService;

    ProductService(ProductRepository repository, CacheService cacheService) {
        this.repository = repository;
        this.cacheService = cacheService;
    }

    Optional<Product> getById(Long id) {
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid product ID");
        }
        return repository.findById(id);
    }

    List<Product> getAll() {
        return repository.findAll();
    }

    Product create(Product product) {
        return repository.save(product);
    }

    Product update(Product product) {
        if (!repository.existsById(product.getId())) {
            throw new EntityNotFoundException("Product not found");
        }
        return repository.save(product);
    }
}

class EntityNotFoundException extends RuntimeException {
    EntityNotFoundException(String message) { super(message); }
}
