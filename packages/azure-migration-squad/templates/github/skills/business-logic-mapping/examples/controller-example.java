// =============================================================================
// Java EE to Spring Boot Controller Conversion Example
// =============================================================================

// -----------------------------------------------------------------------------
// BEFORE: Java EE JAX-RS Resource (com/example/resources/ProductResource.java)
// -----------------------------------------------------------------------------
/*
package com.example.resources;

import com.example.models.Product;
import com.example.services.ProductService;

import javax.ejb.EJB;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.List;

@Path("/products")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ProductResource {

    @EJB
    private ProductService productService;

    @GET
    public List<Product> getAllProducts() {
        return productService.getAllProducts();
    }

    @GET
    @Path("/{id}")
    public Response getProduct(@PathParam("id") Long id) {
        Product product = productService.getProductById(id);
        
        if (product == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        
        return Response.ok(product).build();
    }

    @POST
    public Response createProduct(Product product) {
        Product created = productService.createProduct(product);
        return Response.status(Response.Status.CREATED)
                .entity(created)
                .build();
    }

    @PUT
    @Path("/{id}")
    public Response updateProduct(@PathParam("id") Long id, Product product) {
        Product updated = productService.updateProduct(id, product);
        
        if (updated == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        
        return Response.ok(updated).build();
    }

    @DELETE
    @Path("/{id}")
    public Response deleteProduct(@PathParam("id") Long id) {
        boolean deleted = productService.deleteProduct(id);
        
        if (!deleted) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        
        return Response.noContent().build();
    }

    @GET
    @Path("/search")
    public List<Product> searchProducts(
            @QueryParam("query") String query,
            @QueryParam("categoryId") Long categoryId,
            @QueryParam("minPrice") Double minPrice,
            @QueryParam("maxPrice") Double maxPrice) {
        
        return productService.searchProducts(query, categoryId, minPrice, maxPrice);
    }
}
*/

// -----------------------------------------------------------------------------
// AFTER: Spring Boot REST Controller (com/example/controller/ProductController.java)
// -----------------------------------------------------------------------------

package com.example.controller;

import com.example.dto.CreateProductDto;
import com.example.dto.UpdateProductDto;
import com.example.dto.ProductSearchFilters;
import com.example.model.Product;
import com.example.service.ProductService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    private static final Logger log = LoggerFactory.getLogger(ProductController.class);
    
    private final ProductService productService;

    // Constructor injection (replaces @EJB)
    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    // GET /api/products
    @GetMapping
    public ResponseEntity<List<Product>> getAllProducts() {
        List<Product> products = productService.getAllProducts();
        return ResponseEntity.ok(products);
    }

    // GET /api/products/{id}
    @GetMapping("/{id}")
    public ResponseEntity<Product> getProduct(@PathVariable Long id) {
        return productService.getProductById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // POST /api/products
    @PostMapping
    public ResponseEntity<Product> createProduct(@Valid @RequestBody CreateProductDto dto) {
        Product created = productService.createProduct(dto);
        log.info("Product created: {}", created.getId());
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    // PUT /api/products/{id}
    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(
            @PathVariable Long id,
            @Valid @RequestBody UpdateProductDto dto) {
        
        return productService.updateProduct(id, dto)
                .map(product -> {
                    log.info("Product updated: {}", id);
                    return ResponseEntity.ok(product);
                })
                .orElse(ResponseEntity.notFound().build());
    }

    // DELETE /api/products/{id}
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        if (productService.deleteProduct(id)) {
            log.info("Product deleted: {}", id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }

    // GET /api/products/search
    @GetMapping("/search")
    public ResponseEntity<List<Product>> searchProducts(
            @RequestParam String query,
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) Double minPrice,
            @RequestParam(required = false) Double maxPrice) {
        
        ProductSearchFilters filters = new ProductSearchFilters(categoryId, minPrice, maxPrice);
        List<Product> results = productService.searchProducts(query, filters);
        return ResponseEntity.ok(results);
    }
}

// -----------------------------------------------------------------------------
// DTO for Create (dto/CreateProductDto.java)
// -----------------------------------------------------------------------------

package com.example.dto;

import jakarta.validation.constraints.*;
import java.math.BigDecimal;

public record CreateProductDto(
    @NotBlank
    @Size(max = 255)
    String name,

    @NotNull
    @DecimalMin("0.00")
    BigDecimal price,

    String description
) {}

// -----------------------------------------------------------------------------
// DTO for Update (dto/UpdateProductDto.java)
// -----------------------------------------------------------------------------

package com.example.dto;

import jakarta.validation.constraints.*;
import java.math.BigDecimal;

public record UpdateProductDto(
    @NotBlank
    @Size(max = 255)
    String name,

    @NotNull
    @DecimalMin("0.00")
    BigDecimal price,

    String description
) {}

// -----------------------------------------------------------------------------
// Search Filters DTO (dto/ProductSearchFilters.java)
// -----------------------------------------------------------------------------

package com.example.dto;

public record ProductSearchFilters(
    Long categoryId,
    Double minPrice,
    Double maxPrice
) {}

// -----------------------------------------------------------------------------
// KEY CONVERSION NOTES:
// -----------------------------------------------------------------------------
// 1. @Path → @RequestMapping / @GetMapping / @PostMapping etc.
// 2. @EJB → Constructor injection (Spring manages beans)
// 3. @PathParam → @PathVariable
// 4. @QueryParam → @RequestParam
// 5. Response.ok() → ResponseEntity.ok()
// 6. Response.status(NOT_FOUND) → ResponseEntity.notFound()
// 7. Response.status(CREATED) → ResponseEntity.status(HttpStatus.CREATED)
// 8. MediaType annotations → Spring handles JSON by default
// 9. Add @Valid for request body validation
// 10. Use Optional for nullable returns from service
// 11. Use Java records for DTOs (immutable, concise)
// 12. Add SLF4J logging (replaces custom logging)
