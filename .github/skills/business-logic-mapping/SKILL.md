---
name: business-logic-mapping
description: |
  Business logic discovery, mapping, and preservation during application migration.
  **Use when:** Migrating .NET or Java applications and need to ensure all business logic is preserved.
  **Triggers on:** Phase 2 code migration, business rule identification, logic preservation verification.
  **Covers:** Business rule extraction, logic mapping between source/target, validation tracking, media asset preservation.
  **Critical:** Ensures no business logic is lost during migration by creating traceable mappings.
---

# Business Logic Mapping Skill

Use this skill to discover, map, track, and verify business logic preservation during application migration. This ensures that all business rules, calculations, validations, workflows, and media assets from the legacy application are correctly implemented in the modernized version.

## When to Use This Skill

- Migrating .NET Framework to .NET 8+ applications
- Migrating Java EE to Spring Boot applications
- Any migration where business logic preservation is critical
- When you need to track what logic has been migrated vs. what remains

## Business Logic Discovery

### Step 1: Identify Business Logic Locations

Scan the legacy application for business logic in these common locations:

#### .NET Applications
| Location | What to Look For |
|----------|------------------|
| `Services/` | Business service classes with domain logic |
| `Domain/` or `Models/` | Entity classes with business methods |
| `BusinessLogic/` or `BLL/` | Dedicated business logic layer |
| `Helpers/` or `Utilities/` | Calculation and validation helpers |
| `Validators/` | Business rule validators |
| `Specifications/` | Specification pattern implementations |
| `Rules/` or `Policies/` | Business rule engines |
| Controllers with logic | Logic that should be in services |
| Stored Procedures | Database-embedded business logic |
| Views with logic | Presentation layer calculations |

#### Java Applications
| Location | What to Look For |
|----------|------------------|
| `service/` or `services/` | Business service classes |
| `domain/` | Domain entities with behavior |
| `businesslogic/` or `bll/` | Dedicated business layer |
| `util/` or `helper/` | Utility calculations |
| `validator/` | Validation logic |
| `specification/` | Specification pattern |
| `rule/` or `policy/` | Business rules |
| EJB beans | Enterprise JavaBeans with business logic |
| Stored Procedures | Database business logic |

### Step 2: Categorize Business Logic Types

| Category | Description | Examples |
|----------|-------------|----------|
| **Calculations** | Mathematical/financial computations | Tax calculation, pricing, discounts |
| **Validations** | Business rule validations | Credit limit checks, age verification |
| **Workflows** | Process flows and state machines | Order processing, approval chains |
| **Transformations** | Data transformations | Format conversions, aggregations |
| **Integrations** | External system interactions | Payment gateways, shipping APIs |
| **Authorization** | Business-level permissions | Role-based access, ownership checks |
| **Notifications** | Event-driven communications | Email triggers, alerts |
| **Scheduling** | Time-based business rules | Batch jobs, scheduled reports |

## Business Logic Mapping Document

Create a `reports/Business-Logic-Mapping.md` file to track all business logic:

```markdown
# Business Logic Mapping Report

**Application:** [Application Name]
**Generated:** [Date/Time]
**Migration:** [Source Framework] → [Target Framework]

## Executive Summary
- **Total Business Logic Items:** [Count]
- **Migrated:** [Count] ([Percentage]%)
- **In Progress:** [Count]
- **Pending:** [Count]
- **Blocked:** [Count]

## Business Logic Inventory

### Calculations

| ID | Name | Source Location | Target Location | Status | Verified |
|----|------|-----------------|-----------------|--------|----------|
| BL-001 | Tax Calculation | `OrderService.CalculateTax()` | `Services/TaxCalculator.cs` | ✅ Migrated | ✅ Yes |
| BL-002 | Discount Engine | `PricingHelper.ApplyDiscount()` | `Services/PricingService.cs` | 🔄 In Progress | ⬜ No |
| BL-003 | Shipping Cost | `ShippingCalculator.GetRate()` | Pending | ⬜ Pending | ⬜ No |

### Validations

| ID | Name | Source Location | Target Location | Status | Verified |
|----|------|-----------------|-----------------|--------|----------|
| BL-010 | Credit Limit Check | `CustomerValidator.CheckCredit()` | `Validators/CreditValidator.cs` | ✅ Migrated | ✅ Yes |
| BL-011 | Age Verification | `OrderValidator.VerifyAge()` | `Validators/AgeValidator.cs` | ✅ Migrated | ⬜ No |

### Workflows

| ID | Name | Source Location | Target Location | Status | Verified |
|----|------|-----------------|-----------------|--------|----------|
| BL-020 | Order Processing | `OrderWorkflow.Process()` | `Workflows/OrderStateMachine.cs` | 🔄 In Progress | ⬜ No |
| BL-021 | Approval Chain | `ApprovalService.Submit()` | Pending | ⬜ Pending | ⬜ No |

### Transformations

| ID | Name | Source Location | Target Location | Status | Verified |
|----|------|-----------------|-----------------|--------|----------|
| BL-030 | Report Aggregation | `ReportHelper.Aggregate()` | `Services/ReportingService.cs` | ✅ Migrated | ✅ Yes |

### Integrations

| ID | Name | Source Location | Target Location | Status | Verified |
|----|------|-----------------|-----------------|--------|----------|
| BL-040 | Payment Gateway | `PaymentService.Process()` | `Services/PaymentService.cs` | 🔄 In Progress | ⬜ No |

## Media and Static Assets

| Asset Type | Source Path | Target Path | Status |
|------------|-------------|-------------|--------|
| Images | `/Content/images/` | `/wwwroot/images/` | ✅ Copied |
| CSS | `/Content/css/` | `/wwwroot/css/` | ✅ Copied |
| JavaScript | `/Scripts/` | `/wwwroot/js/` | ✅ Copied |
| Documents | `/App_Data/docs/` | `/wwwroot/docs/` | ✅ Copied |
| Uploads | `/Uploads/` | Azure Blob Storage | 🔄 In Progress |

## Migration Notes

### Preserved As-Is
- [List items that required no changes]

### Modified During Migration
- [List items that required adaptation with explanation]

### Architectural Changes
- [List items that required redesign with justification]

## Verification Checklist
- [ ] All calculations produce same results as legacy
- [ ] All validations enforce same rules
- [ ] All workflows follow same process flows
- [ ] All integrations maintain same behavior
- [ ] All media assets accessible in new application
```

## Business Logic Patterns: .NET Framework → .NET 8

### Service Layer Mapping

```csharp
// =============================================================================
// LEGACY: .NET Framework Service
// =============================================================================
public class OrderService
{
    private readonly OrderRepository _orderRepository;
    
    public decimal CalculateTotal(Order order)
    {
        var subtotal = order.Items.Sum(i => i.Price * i.Quantity);
        var tax = subtotal * 0.08m; // 8% tax
        var discount = GetCustomerDiscount(order.CustomerId);
        return subtotal + tax - discount;
    }
    
    private decimal GetCustomerDiscount(int customerId)
    {
        // Business rule: VIP customers get 10% discount
        var customer = _customerRepository.GetById(customerId);
        return customer.IsVip ? subtotal * 0.10m : 0;
    }
}

// =============================================================================
// MODERN: .NET 8 Service (Preserve same logic, modernize patterns)
// =============================================================================
public interface IOrderCalculationService
{
    decimal CalculateTotal(Order order);
}

public class OrderCalculationService : IOrderCalculationService
{
    private readonly ICustomerRepository _customerRepository;
    private readonly IOptions<TaxSettings> _taxSettings;
    private readonly ILogger<OrderCalculationService> _logger;

    public OrderCalculationService(
        ICustomerRepository customerRepository,
        IOptions<TaxSettings> taxSettings,
        ILogger<OrderCalculationService> logger)
    {
        _customerRepository = customerRepository;
        _taxSettings = taxSettings;
        _logger = logger;
    }

    public decimal CalculateTotal(Order order)
    {
        // PRESERVED: Same calculation logic
        var subtotal = order.Items.Sum(i => i.Price * i.Quantity);
        var tax = subtotal * _taxSettings.Value.DefaultRate; // Externalized config
        var discount = GetCustomerDiscount(order.CustomerId, subtotal);
        
        _logger.LogDebug("Order total calculated: Subtotal={Subtotal}, Tax={Tax}, Discount={Discount}", 
            subtotal, tax, discount);
        
        return subtotal + tax - discount;
    }
    
    private decimal GetCustomerDiscount(int customerId, decimal subtotal)
    {
        // PRESERVED: Same business rule - VIP customers get 10% discount
        var customer = _customerRepository.GetById(customerId);
        return customer?.IsVip == true ? subtotal * 0.10m : 0;
    }
}
```

### Validation Logic Mapping

```csharp
// =============================================================================
// LEGACY: .NET Framework Validator
// =============================================================================
public class OrderValidator
{
    public ValidationResult Validate(Order order)
    {
        var errors = new List<string>();
        
        // Business Rule: Minimum order amount
        if (order.Total < 10.00m)
            errors.Add("Minimum order amount is $10.00");
        
        // Business Rule: Maximum items per order
        if (order.Items.Count > 100)
            errors.Add("Maximum 100 items per order");
        
        // Business Rule: Customer credit check
        if (!HasSufficientCredit(order.CustomerId, order.Total))
            errors.Add("Insufficient credit limit");
        
        return new ValidationResult(errors);
    }
}

// =============================================================================
// MODERN: .NET 8 with FluentValidation (Same rules, modern pattern)
// =============================================================================
public class OrderValidator : AbstractValidator<Order>
{
    private readonly ICustomerCreditService _creditService;

    public OrderValidator(ICustomerCreditService creditService)
    {
        _creditService = creditService;

        // PRESERVED: Minimum order amount
        RuleFor(x => x.Total)
            .GreaterThanOrEqualTo(10.00m)
            .WithMessage("Minimum order amount is $10.00");

        // PRESERVED: Maximum items per order
        RuleFor(x => x.Items.Count)
            .LessThanOrEqualTo(100)
            .WithMessage("Maximum 100 items per order");

        // PRESERVED: Customer credit check
        RuleFor(x => x)
            .MustAsync(async (order, cancellation) => 
                await _creditService.HasSufficientCreditAsync(order.CustomerId, order.Total))
            .WithMessage("Insufficient credit limit");
    }
}
```

## Business Logic Patterns: Java EE → Spring Boot

### EJB to Spring Service

```java
// =============================================================================
// LEGACY: Java EE EJB
// =============================================================================
@Stateless
public class InvoiceServiceBean implements InvoiceService {
    
    @EJB
    private CustomerDAO customerDAO;
    
    @EJB
    private TaxCalculator taxCalculator;
    
    public Invoice generateInvoice(Order order) {
        // Business logic: Calculate invoice with tax
        BigDecimal subtotal = calculateSubtotal(order);
        BigDecimal tax = taxCalculator.calculate(subtotal, order.getState());
        BigDecimal total = subtotal.add(tax);
        
        // Business rule: Apply early payment discount
        if (order.getPaymentTerms().equals("NET10")) {
            total = applyEarlyPaymentDiscount(total, new BigDecimal("0.02"));
        }
        
        return new Invoice(order.getId(), subtotal, tax, total);
    }
    
    private BigDecimal applyEarlyPaymentDiscount(BigDecimal amount, BigDecimal rate) {
        return amount.multiply(BigDecimal.ONE.subtract(rate));
    }
}

// =============================================================================
// MODERN: Spring Boot Service (Same logic preserved)
// =============================================================================
@Service
@Transactional
public class InvoiceService {
    
    private final CustomerRepository customerRepository;
    private final TaxCalculationService taxCalculator;
    private final Logger log = LoggerFactory.getLogger(InvoiceService.class);
    
    public InvoiceService(CustomerRepository customerRepository, 
                          TaxCalculationService taxCalculator) {
        this.customerRepository = customerRepository;
        this.taxCalculator = taxCalculator;
    }
    
    public Invoice generateInvoice(Order order) {
        // PRESERVED: Same calculation logic
        BigDecimal subtotal = calculateSubtotal(order);
        BigDecimal tax = taxCalculator.calculate(subtotal, order.getState());
        BigDecimal total = subtotal.add(tax);
        
        // PRESERVED: Same business rule - early payment discount
        if ("NET10".equals(order.getPaymentTerms())) {
            total = applyEarlyPaymentDiscount(total, new BigDecimal("0.02"));
            log.debug("Applied 2% early payment discount for order {}", order.getId());
        }
        
        return new Invoice(order.getId(), subtotal, tax, total);
    }
    
    private BigDecimal applyEarlyPaymentDiscount(BigDecimal amount, BigDecimal rate) {
        // PRESERVED: Exact same calculation
        return amount.multiply(BigDecimal.ONE.subtract(rate));
    }
}
```

## Media and Asset Preservation

### Asset Types to Track

| Asset Type | .NET Framework Location | .NET 8 Location | Notes |
|------------|------------------------|-----------------|-------|
| Images | `/Content/images/` | `/wwwroot/images/` | Copy as-is |
| CSS | `/Content/css/` | `/wwwroot/css/` | May need path updates |
| JavaScript | `/Scripts/` | `/wwwroot/js/` | Check for bundle references |
| Fonts | `/Content/fonts/` | `/wwwroot/fonts/` | Copy as-is |
| Documents | `/App_Data/` | `/wwwroot/` or Azure Blob | Consider cloud storage |
| User Uploads | `/Uploads/` | Azure Blob Storage | Migrate to cloud |
| Email Templates | `/Templates/` | `/Templates/` or embedded | Keep same structure |
| Report Templates | `/Reports/` | `/Reports/` | Crystal Reports → SSRS/alternatives |

### Asset Migration Checklist

```markdown
## Asset Migration Verification

### Static Files
- [ ] All images copied to wwwroot/images
- [ ] All CSS files copied and paths updated
- [ ] All JavaScript files copied and bundle references updated
- [ ] Favicon and icons present
- [ ] Fonts copied and CSS @font-face paths updated

### Dynamic Content
- [ ] Upload directory strategy defined (local vs. Azure Blob)
- [ ] Existing uploads migrated or migration plan in place
- [ ] Image processing libraries updated (System.Drawing → ImageSharp)

### Templates
- [ ] Email templates preserved and tested
- [ ] PDF generation templates migrated
- [ ] Report templates converted or alternative chosen

### Configuration Files
- [ ] XML configs transformed to JSON
- [ ] Resource files (.resx) migrated
- [ ] Localization files preserved
```

## Verification Strategies

### Unit Test Generation for Business Logic

For each business logic item, generate a verification test:

```csharp
// Test to verify business logic preservation
[Fact]
public void CalculateTotal_WithVipCustomer_AppliesTenPercentDiscount()
{
    // Arrange - Same inputs as legacy system test
    var order = new Order
    {
        CustomerId = 123, // VIP customer
        Items = new List<OrderItem>
        {
            new() { Price = 100m, Quantity = 1 }
        }
    };
    
    // Act
    var total = _orderService.CalculateTotal(order);
    
    // Assert - Must match legacy system output
    // Subtotal: 100, Tax (8%): 8, Discount (10%): 10, Total: 98
    Assert.Equal(98.00m, total);
}
```

### Comparison Testing

```csharp
// Run same input through legacy and modern systems, compare outputs
[Theory]
[MemberData(nameof(GetLegacyTestCases))]
public void ModernSystem_ProducesSameOutput_AsLegacy(
    TestInput input, 
    LegacyOutput expectedOutput)
{
    // Act
    var modernOutput = _modernService.Process(input);
    
    // Assert - Outputs must match
    Assert.Equal(expectedOutput.Result, modernOutput.Result);
    Assert.Equal(expectedOutput.SideEffects, modernOutput.SideEffects);
}
```

## Tracking During Migration

### Status Codes

| Status | Icon | Meaning |
|--------|------|---------|
| Pending | ⬜ | Not yet started |
| In Progress | 🔄 | Currently being migrated |
| Migrated | ✅ | Migration complete |
| Verified | ✅✅ | Migration verified with tests |
| Blocked | 🚫 | Cannot migrate, needs decision |
| Modified | ⚠️ | Logic changed (documented) |

### Update Protocol

After each migration session, update the Business-Logic-Mapping.md:

1. **Mark completed items** with status change
2. **Add new discoveries** to the inventory
3. **Document any modifications** with justification
4. **Update verification status** after testing
5. **Note blockers** with required decisions

## Integration with Migration Phases

### Phase 1 (Assessment)
- Create initial Business-Logic-Mapping.md
- Identify all business logic locations
- Categorize by type and complexity
- Estimate migration effort per item

### Phase 2 (Code Migration)
- Reference mapping during migration
- Update status as items are migrated
- Preserve logic exactly unless documented
- Generate verification tests

### Phase 3+ (Infrastructure/Deploy)
- Verify media assets are accessible
- Confirm cloud storage for uploads
- Test integrations end-to-end

## Templates and Examples

See the [examples](./examples/) directory for:

### Report Template
- [Business-Logic-Mapping-Template.md](./examples/Business-Logic-Mapping-Template.md) - Copy to `reports/` and fill in during migration

### .NET Code Conversion Examples
- [controller-example.cs](./examples/controller-example.cs) - .NET Framework MVC to .NET 8 controller
- [service-example.cs](./examples/service-example.cs) - .NET Framework service to .NET 8 with caching and logging
- [model-example.cs](./examples/model-example.cs) - EF6 entity to EF Core with business methods

### Java Code Conversion Examples
- [controller-example.java](./examples/controller-example.java) - Java EE JAX-RS to Spring Boot REST controller
- [service-example.java](./examples/service-example.java) - EJB to Spring Boot service with business logic preservation
- [model-example.java](./examples/model-example.java) - Java EE JPA to Spring Boot JPA entity with business methods
