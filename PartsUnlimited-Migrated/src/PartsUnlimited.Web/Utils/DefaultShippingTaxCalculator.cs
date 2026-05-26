using System.Collections.Generic;
using System.Linq;
using PartsUnlimited.Models;

namespace PartsUnlimited.Utils
{
    public class DefaultShippingTaxCalculator : IShippingTaxCalculator
    {
        public OrderCostSummary CalculateCost(IEnumerable<ILineItem> items, string postalCode)
        {
            decimal subTotal = 0, tax = 0, shipping = 0, total = 0;
            int itemsCount = 0;
            if (items != null)
            {
                subTotal = items.Sum(x => x.Count * x.Product.Price);
                itemsCount = items.Sum(x => x.Count);
                shipping = CalculateShipping(itemsCount);
                tax = CalculateTax(subTotal + shipping, postalCode);
                total = subTotal + shipping + tax;
            }

            return new OrderCostSummary
            {
                CartSubTotal = subTotal.ToString("C"),
                CartShipping = shipping.ToString("C"),
                CartTax = tax.ToString("C"),
                CartTotal = total.ToString("C")
            };
        }

        protected decimal CalculateTax(decimal taxable, string postalCode = null)
        {
            var taxRate = 0.06m;
            if (!string.IsNullOrEmpty(postalCode) && postalCode.StartsWith("98"))
            {
                taxRate = 0.075m;
            }
            return taxable * taxRate;
        }

        protected decimal CalculateShipping(int itemsCount)
        {
            return itemsCount * 5.0m;
        }
    }
}
