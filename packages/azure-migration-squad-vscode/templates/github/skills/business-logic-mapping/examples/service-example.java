// =============================================================================
// Java EE EJB to Spring Boot Service Conversion Example
// =============================================================================

// -----------------------------------------------------------------------------
// BEFORE: Java EE Stateless EJB (com/example/services/ProductServiceBean.java)
// -----------------------------------------------------------------------------
/*
package com.example.services;

import com.example.models.Product;
import com.example.dao.ProductDAO;

import javax.ejb.Stateless;
import javax.ejb.EJB;
import javax.inject.Inject;
import java.util.List;
import java.util.logging.Logger;

@Stateless
public class ProductServiceBean implements ProductService {

    private static final Logger LOGGER = Logger.getLogger(ProductServiceBean.class.getName());

    @EJB
    private ProductDAO productDAO;

    @Override
    public List<Product> getAllProducts() {
        LOGGER.info("Fetching all products from database");
        return productDAO.findAll();
    }

    @Override
    public Product getProductById(Long id) {
        return productDAO.findById(id);
    }

    @Override
    public Product createProduct(Product product) {
        product.setCreatedAt(new java.util.Date());
        productDAO.persist(product);
        LOGGER.info("Product created: " + product.getId());
        return product;
    }

    @Override
    public Product updateProduct(Long id, Product productData) {
        Product existing = productDAO.findById(id);
        if (existing == null) {
            return null;
        }

        existing.setName(productData.getName());
        existing.setPrice(productData.getPrice());
        existing.setDescription(productData.getDescription());
        existing.setUpdatedAt(new java.util.Date());

        productDAO.merge(existing);
        LOGGER.info("Product updated: " + id);
        return existing;
    }

    @Override
    public boolean deleteProduct(Long id) {
        Product existing = productDAO.findById(id);
        if (existing == null) {
            return false;
        }

        productDAO.remove(existing);
        LOGGER.info("Product deleted: " + id);
        return true;
    }

    @Override
    public List<Product> searchProducts(String query, Long categoryId, 
                                         Double minPrice, Double maxPrice) {
        // Complex query building with JPQL
        StringBuilder jpql = new StringBuilder("SELECT p FROM Product p WHERE p.name LIKE :query");
        
        if (categoryId != null) {
            jpql.append(" AND p.category.id = :categoryId");
        }
        if (minPrice != null) {
            jpql.append(" AND p.price >= :minPrice");
        }
        if (maxPrice != null) {
            jpql.append(" AND p.price <= :maxPrice");
        }
        
        // Execute with parameters...
        return productDAO.executeQuery(jpql.toString(), query, categoryId, minPrice, maxPrice);
    }

    // Business Logic: Calculate discounted price
    @Override
    public java.math.BigDecimal calculateDiscountedPrice(Long productId, int discountPercent) {
        Product product = productDAO.findById(productId);
        if (product == null) {
            throw new IllegalArgumentException("Product not found: " + productId);
        }
        
        // BUSINESS RULE: Maximum discount is 50%
        if (discountPercent > 50) {
            discountPercent = 50;
        }
        
        java.math.BigDecimal discount = product.getPrice()
            .multiply(java.math.BigDecimal.valueOf(discountPercent))
            .divide(java.math.BigDecimal.valueOf(100));
        
        return product.getPrice().subtract(discount);
    }

    // Business Logic: Check if product is available
    @Override
    public boolean isProductAvailable(Long productId) {
        Product product = productDAO.findById(productId);
        if (product == null) {
            return false;
        }
        
        // BUSINESS RULE: Product is available if active and in stock
        return product.isActive() && product.getStockQuantity() > 0;
    }
}
*/

// -----------------------------------------------------------------------------
// AFTER: Spring Boot Service Interface (com/example/service/ProductService.java)
// -----------------------------------------------------------------------------

package com.example.service;

import com.example.dto.CreateProductDto;
import com.example.dto.UpdateProductDto;
import com.example.dto.ProductSearchFilters;
import com.example.model.Product;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

public interface ProductService {
    List<Product> getAllProducts();
    Optional<Product> getProductById(Long id);
    Product createProduct(CreateProductDto dto);
    Optional<Product> updateProduct(Long id, UpdateProductDto dto);
    boolean deleteProduct(Long id);
    List<Product> searchProducts(String query, ProductSearchFilters filters);
    
    // Business logic methods
    BigDecimal calculateDiscountedPrice(Long productId, int discountPercent);
    boolean isProductAvailable(Long productId);
}

// -----------------------------------------------------------------------------
// AFTER: Spring Boot Service Implementation (com/example/service/ProductServiceImpl.java)
// -----------------------------------------------------------------------------

package com.example.service;

import com.example.dto.CreateProductDto;
import com.example.dto.UpdateProductDto;
import com.example.dto.ProductSearchFilters;
import com.example.exception.ProductNotFoundException;
import com.example.model.Product;
import com.example.repository.ProductRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class ProductServiceImpl implements ProductService {

    private static final Logger log = LoggerFactory.getLogger(ProductServiceImpl.class);
    
    private final ProductRepository productRepository;

    // Constructor injection (replaces @EJB)
    public ProductServiceImpl(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Override
    @Cacheable("products")
    @Transactional(readOnly = true)
    public List<Product> getAllProducts() {
        log.info("Fetching all products from database");
        return productRepository.findAll();
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Product> getProductById(Long id) {
        return productRepository.findById(id);
    }

    @Override
    @CacheEvict(value = "products", allEntries = true)
    public Product createProduct(CreateProductDto dto) {
        Product product = new Product();
        product.setName(dto.name());
        product.setPrice(dto.price());
        product.setDescription(dto.description());
        product.setCreatedAt(LocalDateTime.now());
        
        Product saved = productRepository.save(product);
        log.info("Product created: {}", saved.getId());
        return saved;
    }

    @Override
    @CacheEvict(value = "products", allEntries = true)
    public Optional<Product> updateProduct(Long id, UpdateProductDto dto) {
        return productRepository.findById(id)
                .map(existing -> {
                    existing.setName(dto.name());
                    existing.setPrice(dto.price());
                    existing.setDescription(dto.description());
                    existing.setUpdatedAt(LocalDateTime.now());
                    
                    Product updated = productRepository.save(existing);
                    log.info("Product updated: {}", id);
                    return updated;
                });
    }

    @Override
    @CacheEvict(value = "products", allEntries = true)
    public boolean deleteProduct(Long id) {
        if (productRepository.existsById(id)) {
            productRepository.deleteById(id);
            log.info("Product deleted: {}", id);
            return true;
        }
        return false;
    }

    @Override
    @Transactional(readOnly = true)
    public List<Product> searchProducts(String query, ProductSearchFilters filters) {
        // Use Spring Data JPA Specifications or custom repository method
        return productRepository.searchProducts(
                query,
                filters.categoryId(),
                filters.minPrice(),
                filters.maxPrice()
        );
    }

    // =========================================================================
    // PRESERVED BUSINESS LOGIC
    // =========================================================================

    @Override
    @Transactional(readOnly = true)
    public BigDecimal calculateDiscountedPrice(Long productId, int discountPercent) {
        Product product = productRepository.findById(productId)
                .orElseThrow(() -> new ProductNotFoundException("Product not found: " + productId));
        
        // PRESERVED BUSINESS RULE: Maximum discount is 50%
        int effectiveDiscount = Math.min(discountPercent, 50);
        
        BigDecimal discountAmount = product.getPrice()
                .multiply(BigDecimal.valueOf(effectiveDiscount))
                .divide(BigDecimal.valueOf(100), RoundingMode.HALF_UP);
        
        return product.getPrice().subtract(discountAmount);
    }

    @Override
    @Transactional(readOnly = true)
    public boolean isProductAvailable(Long productId) {
        return productRepository.findById(productId)
                .map(product -> {
                    // PRESERVED BUSINESS RULE: Product is available if active and in stock
                    return product.isActive() && product.getStockQuantity() > 0;
                })
                .orElse(false);
    }
}

// -----------------------------------------------------------------------------
// Custom Repository Method (repository/ProductRepository.java)
// -----------------------------------------------------------------------------

package com.example.repository;

import com.example.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {

    // Custom search query (replaces manual JPQL building)
    @Query("""
        SELECT p FROM Product p 
        WHERE p.name LIKE %:query%
        AND (:categoryId IS NULL OR p.category.id = :categoryId)
        AND (:minPrice IS NULL OR p.price >= :minPrice)
        AND (:maxPrice IS NULL OR p.price <= :maxPrice)
        """)
    List<Product> searchProducts(
            @Param("query") String query,
            @Param("categoryId") Long categoryId,
            @Param("minPrice") Double minPrice,
            @Param("maxPrice") Double maxPrice
    );

    // Spring Data derived query methods
    List<Product> findByActiveTrue();
    List<Product> findByCategoryId(Long categoryId);
    List<Product> findByPriceBetween(BigDecimal min, BigDecimal max);
}

// -----------------------------------------------------------------------------
// Custom Exception (exception/ProductNotFoundException.java)
// -----------------------------------------------------------------------------

package com.example.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class ProductNotFoundException extends RuntimeException {
    public ProductNotFoundException(String message) {
        super(message);
    }
}

// -----------------------------------------------------------------------------
// Enable Caching (config/CacheConfig.java)
// -----------------------------------------------------------------------------
/*
package com.example.config;

import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableCaching
public class CacheConfig {
    // Cache configuration
}
*/

// -----------------------------------------------------------------------------
// KEY CONVERSION NOTES:
// -----------------------------------------------------------------------------
// 1. @Stateless → @Service + @Transactional
// 2. @EJB → Constructor injection
// 3. java.util.logging.Logger → SLF4J Logger
// 4. java.util.Date → java.time.LocalDateTime
// 5. ProductDAO → Spring Data JPA Repository
// 6. persist/merge/remove → save/deleteById
// 7. Manual JPQL → @Query annotation or derived methods
// 8. Return null → Return Optional<T>
// 9. Manual caching → @Cacheable/@CacheEvict annotations
// 10. BUSINESS LOGIC PRESERVED: Same rules, modern syntax
// 11. Add @Transactional(readOnly = true) for read operations
// 12. Use record types for DTOs (immutable)
