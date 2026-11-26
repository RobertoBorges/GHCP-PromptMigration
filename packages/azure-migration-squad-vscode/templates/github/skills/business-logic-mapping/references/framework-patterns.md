# Business Logic Framework Examples

Use only the section for the application stack being migrated. These examples are illustrative; preserve behavior discovered in the source rather than copying sample business rules.

## Business Logic Patterns: .NET Framework → .NET 10

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
// MODERN: .NET 10 Service (Preserve same logic, modernize patterns)
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
// MODERN: .NET 10 with FluentValidation (Same rules, modern pattern)
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
