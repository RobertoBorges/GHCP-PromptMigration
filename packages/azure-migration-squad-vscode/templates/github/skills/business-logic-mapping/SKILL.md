---
name: business-logic-mapping
description: |
  Business logic discovery, mapping, and preservation during application migration across languages and runtimes.
  **Use when:** Migrating an application and need to ensure its business logic and assets are preserved.
  **Triggers on:** Phase 2 code migration, business rule identification, logic preservation verification.
  **Covers:** Business rule extraction, logic mapping between source/target, validation tracking, media asset preservation.
  **Critical:** Ensures no business logic is lost during migration by creating traceable mappings.
user-invocable: false
---

# Business Logic Mapping Skill

Use this skill to discover, map, track, and verify business logic preservation during application migration. This ensures that all business rules, calculations, validations, workflows, and media assets from the legacy application are correctly implemented in the modernized version.

## When to Use This Skill

- Migrating applications of any supported language or runtime
- Translating legacy .NET or Java logic using the stack-specific examples
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

Create `reports/Business-Logic-Mapping.md` to track each discovered rule from its source location to its target implementation, with status and verification evidence. Start from the [report template](./examples/Business-Logic-Mapping-Template.md); include calculations, validations, workflows, transformations, integrations, media assets, and documented exceptions as applicable.

## Framework Examples

For detailed .NET and Java before/after code patterns, load [framework examples](./references/framework-patterns.md) only when that stack applies.

## Media and Asset Preservation

### Asset Types to Track

| Asset Type | .NET Framework Location | .NET 10 Location | Notes |
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
- [controller-example.cs](./examples/controller-example.cs) - .NET Framework MVC to .NET 10 controller
- [service-example.cs](./examples/service-example.cs) - .NET Framework service to .NET 10 with caching and logging
- [model-example.cs](./examples/model-example.cs) - EF6 entity to EF Core with business methods

### Java Code Conversion Examples
- [controller-example.java](./examples/controller-example.java) - Java EE JAX-RS to Spring Boot REST controller
- [service-example.java](./examples/service-example.java) - EJB to Spring Boot service with business logic preservation
- [model-example.java](./examples/model-example.java) - Java EE JPA to Spring Boot JPA entity with business methods
