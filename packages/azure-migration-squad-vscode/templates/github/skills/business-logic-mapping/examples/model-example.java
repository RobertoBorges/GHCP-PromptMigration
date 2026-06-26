// =============================================================================
// Java EE JPA Entity to Spring Boot JPA Entity Conversion Example
// =============================================================================

// -----------------------------------------------------------------------------
// BEFORE: Java EE JPA Entity (com/example/models/Product.java)
// -----------------------------------------------------------------------------
/*
package com.example.models;

import javax.persistence.*;
import javax.validation.constraints.*;
import java.math.BigDecimal;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "products")
@NamedQueries({
    @NamedQuery(name = "Product.findAll", 
                query = "SELECT p FROM Product p"),
    @NamedQuery(name = "Product.findByCategory", 
                query = "SELECT p FROM Product p WHERE p.category.id = :categoryId"),
    @NamedQuery(name = "Product.findActive", 
                query = "SELECT p FROM Product p WHERE p.active = true")
})
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotNull
    @Size(max = 255)
    @Column(nullable = false)
    private String name;

    @NotNull
    @Size(max = 255)
    @Column(nullable = false, unique = true)
    private String slug;

    @Column(columnDefinition = "TEXT")
    private String description;

    @NotNull
    @DecimalMin("0.00")
    @Column(precision = 18, scale = 2, nullable = false)
    private BigDecimal price;

    @Column(name = "is_active")
    private boolean active = true;

    @Column(name = "stock_quantity")
    private int stockQuantity = 0;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "created_at")
    private Date createdAt;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "updated_at")
    private Date updatedAt;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "deleted_at")
    private Date deletedAt;

    // Relationships
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private Category category;

    @OneToMany(mappedBy = "product", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<Review> reviews = new HashSet<>();

    @ManyToMany
    @JoinTable(
        name = "product_tags",
        joinColumns = @JoinColumn(name = "product_id"),
        inverseJoinColumns = @JoinColumn(name = "tag_id")
    )
    private Set<Tag> tags = new HashSet<>();

    // Lifecycle callbacks
    @PrePersist
    protected void onCreate() {
        createdAt = new Date();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = new Date();
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getSlug() { return slug; }
    public void setSlug(String slug) { this.slug = slug; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }
    
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
    
    public int getStockQuantity() { return stockQuantity; }
    public void setStockQuantity(int stockQuantity) { this.stockQuantity = stockQuantity; }
    
    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }
    
    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }
    
    public Date getDeletedAt() { return deletedAt; }
    public void setDeletedAt(Date deletedAt) { this.deletedAt = deletedAt; }
    
    public Category getCategory() { return category; }
    public void setCategory(Category category) { this.category = category; }
    
    public Set<Review> getReviews() { return reviews; }
    public void setReviews(Set<Review> reviews) { this.reviews = reviews; }
    
    public Set<Tag> getTags() { return tags; }
    public void setTags(Set<Tag> tags) { this.tags = tags; }

    // =========================================================================
    // BUSINESS LOGIC METHODS
    // =========================================================================

    // Business Rule: Calculate formatted price for display
    public String getFormattedPrice() {
        return String.format("$%.2f", price);
    }

    // Business Rule: Check if product is available for purchase
    public boolean isAvailable() {
        return active && stockQuantity > 0 && deletedAt == null;
    }

    // Business Rule: Apply discount with maximum cap
    public BigDecimal applyDiscount(int percentage) {
        // Max discount is 50%
        int effectivePercentage = Math.min(percentage, 50);
        BigDecimal discountMultiplier = BigDecimal.ONE
            .subtract(BigDecimal.valueOf(effectivePercentage).divide(BigDecimal.valueOf(100)));
        return price.multiply(discountMultiplier);
    }

    // Business Rule: Check if product needs restock
    public boolean needsRestock(int threshold) {
        return stockQuantity <= threshold;
    }

    // Business Rule: Add review with validation
    public void addReview(Review review) {
        if (review == null) {
            throw new IllegalArgumentException("Review cannot be null");
        }
        reviews.add(review);
        review.setProduct(this);
    }

    // Business Rule: Calculate average rating
    public double getAverageRating() {
        if (reviews.isEmpty()) {
            return 0.0;
        }
        return reviews.stream()
            .mapToInt(Review::getRating)
            .average()
            .orElse(0.0);
    }
}
*/

// -----------------------------------------------------------------------------
// AFTER: Spring Boot JPA Entity (com/example/model/Product.java)
// -----------------------------------------------------------------------------

package com.example.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "products", indexes = {
    @Index(name = "idx_product_slug", columnList = "slug", unique = true),
    @Index(name = "idx_product_category", columnList = "category_id"),
    @Index(name = "idx_product_active", columnList = "is_active")
})
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotNull
    @Size(max = 255)
    @Column(nullable = false)
    private String name;

    @NotNull
    @Size(max = 255)
    @Column(nullable = false, unique = true)
    private String slug;

    @Column(columnDefinition = "TEXT")
    private String description;

    @NotNull
    @DecimalMin("0.00")
    @Column(precision = 18, scale = 2, nullable = false)
    private BigDecimal price;

    @Column(name = "is_active")
    private boolean active = true;

    @Column(name = "stock_quantity")
    private int stockQuantity = 0;

    // Use LocalDateTime instead of Date
    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Column(name = "deleted_at")
    private LocalDateTime deletedAt;

    // Relationships (same pattern, jakarta.persistence)
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private Category category;

    @OneToMany(mappedBy = "product", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<Review> reviews = new HashSet<>();

    @ManyToMany
    @JoinTable(
        name = "product_tags",
        joinColumns = @JoinColumn(name = "product_id"),
        inverseJoinColumns = @JoinColumn(name = "tag_id")
    )
    private Set<Tag> tags = new HashSet<>();

    // Lifecycle callbacks (same pattern)
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    // =========================================================================
    // GETTERS AND SETTERS
    // =========================================================================

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getSlug() { return slug; }
    public void setSlug(String slug) { this.slug = slug; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }
    
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
    
    public int getStockQuantity() { return stockQuantity; }
    public void setStockQuantity(int stockQuantity) { this.stockQuantity = stockQuantity; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    public LocalDateTime getDeletedAt() { return deletedAt; }
    public void setDeletedAt(LocalDateTime deletedAt) { this.deletedAt = deletedAt; }
    
    public Category getCategory() { return category; }
    public void setCategory(Category category) { this.category = category; }
    
    public Set<Review> getReviews() { return reviews; }
    public void setReviews(Set<Review> reviews) { this.reviews = reviews; }
    
    public Set<Tag> getTags() { return tags; }
    public void setTags(Set<Tag> tags) { this.tags = tags; }

    // =========================================================================
    // PRESERVED BUSINESS LOGIC METHODS
    // =========================================================================

    /**
     * PRESERVED: Calculate formatted price for display
     */
    public String getFormattedPrice() {
        return String.format("$%.2f", price);
    }

    /**
     * PRESERVED: Check if product is available for purchase
     * Business Rule: Must be active, in stock, and not deleted
     */
    public boolean isAvailable() {
        return active && stockQuantity > 0 && deletedAt == null;
    }

    /**
     * PRESERVED: Apply discount with maximum cap
     * Business Rule: Maximum discount is 50%
     */
    public BigDecimal applyDiscount(int percentage) {
        int effectivePercentage = Math.min(percentage, 50);
        BigDecimal discountMultiplier = BigDecimal.ONE
            .subtract(BigDecimal.valueOf(effectivePercentage)
                .divide(BigDecimal.valueOf(100), 4, RoundingMode.HALF_UP));
        return price.multiply(discountMultiplier).setScale(2, RoundingMode.HALF_UP);
    }

    /**
     * PRESERVED: Check if product needs restock
     * Business Rule: Needs restock when stock falls to or below threshold
     */
    public boolean needsRestock(int threshold) {
        return stockQuantity <= threshold;
    }

    /**
     * PRESERVED: Add review with validation
     * Business Rule: Review cannot be null, maintains bidirectional relationship
     */
    public void addReview(Review review) {
        if (review == null) {
            throw new IllegalArgumentException("Review cannot be null");
        }
        reviews.add(review);
        review.setProduct(this);
    }

    /**
     * PRESERVED: Calculate average rating from reviews
     * Business Rule: Returns 0.0 if no reviews exist
     */
    public double getAverageRating() {
        if (reviews.isEmpty()) {
            return 0.0;
        }
        return reviews.stream()
            .mapToInt(Review::getRating)
            .average()
            .orElse(0.0);
    }

    /**
     * NEW: Remove review (bidirectional)
     */
    public void removeReview(Review review) {
        reviews.remove(review);
        review.setProduct(null);
    }
}

// -----------------------------------------------------------------------------
// Soft Delete Specification (for global filtering)
// -----------------------------------------------------------------------------

package com.example.repository;

import com.example.model.Product;
import org.springframework.data.jpa.domain.Specification;

public class ProductSpecifications {

    public static Specification<Product> notDeleted() {
        return (root, query, criteriaBuilder) -> 
            criteriaBuilder.isNull(root.get("deletedAt"));
    }

    public static Specification<Product> isActive() {
        return (root, query, criteriaBuilder) -> 
            criteriaBuilder.isTrue(root.get("active"));
    }

    public static Specification<Product> inCategory(Long categoryId) {
        return (root, query, criteriaBuilder) -> 
            criteriaBuilder.equal(root.get("category").get("id"), categoryId);
    }

    public static Specification<Product> priceBetween(BigDecimal min, BigDecimal max) {
        return (root, query, criteriaBuilder) -> 
            criteriaBuilder.between(root.get("price"), min, max);
    }
}

// Usage in service:
// productRepository.findAll(
//     Specification.where(notDeleted())
//         .and(isActive())
//         .and(inCategory(categoryId))
// );

// -----------------------------------------------------------------------------
// KEY CONVERSION NOTES:
// -----------------------------------------------------------------------------
// 1. javax.persistence → jakarta.persistence (Jakarta EE 9+)
// 2. javax.validation → jakarta.validation
// 3. java.util.Date → java.time.LocalDateTime
// 4. @Temporal not needed with LocalDateTime
// 5. @NamedQueries → Spring Data derived methods or @Query
// 6. Business methods PRESERVED exactly as-is
// 7. Same @PrePersist/@PreUpdate callbacks work
// 8. Same relationship mappings work
// 9. Added @Index annotations for performance
// 10. Use Specification pattern for dynamic queries (replaces Criteria API)
// 11. RoundingMode added for precise decimal calculations
// 12. HashSet still works for collections
