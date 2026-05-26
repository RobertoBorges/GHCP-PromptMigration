using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PartsUnlimited.Models;
using PartsUnlimited.Utils;
using PartsUnlimited.ViewModels;

namespace PartsUnlimited.Controllers
{
    [Authorize]
    public class OrdersController : Controller
    {
        private readonly IOrdersQuery _ordersQuery;
        private readonly ITelemetryProvider _telemetry;
        private readonly IShippingTaxCalculator _shippingTaxCalc;

        public OrdersController(IOrdersQuery ordersQuery, ITelemetryProvider telemetryProvider,
            IShippingTaxCalculator shippingTaxCalc)
        {
            _ordersQuery = ordersQuery;
            _telemetry = telemetryProvider;
            _shippingTaxCalc = shippingTaxCalc;
        }

        public async Task<IActionResult> Index(DateTime? start, DateTime? end, string invalidOrderSearch)
        {
            var username = User.Identity!.Name;
            return View(await _ordersQuery.IndexHelperAsync(username, start, end, invalidOrderSearch, false));
        }

        public async Task<IActionResult> Details(int? id)
        {
            if (id == null)
            {
                _telemetry.TrackTrace("Order/Server/NullId");
                return RedirectToAction("Index", new { invalidOrderSearch = Request.Query["id"].ToString() });
            }

            var order = await _ordersQuery.FindOrderAsync(id.Value);
            var username = User.Identity!.Name;

            if (order == null || !string.Equals(order.Username, username, StringComparison.Ordinal))
            {
                _telemetry.TrackTrace("Order/Server/UsernameMismatch");
                return RedirectToAction("Index", new { invalidOrderSearch = id.ToString() });
            }

            var eventProperties = new Dictionary<string, string>
            {
                { "Id", id.ToString() },
                { "Username", username }
            };
            var costSummary = new OrderCostSummary
            {
                CartSubTotal = 0.ToString("C"),
                CartShipping = 0.ToString("C"),
                CartTax = 0.ToString("C"),
                CartTotal = 0.ToString("C")
            };
            if (order.OrderDetails == null)
            {
                _telemetry.TrackEvent("Order/Server/NullDetails", eventProperties, null);
            }
            else
            {
                var eventMeasurements = new Dictionary<string, double>
                {
                    { "LineItemCount", order.OrderDetails.Count }
                };
                _telemetry.TrackEvent("Order/Server/Details", eventProperties, eventMeasurements);

                costSummary = _shippingTaxCalc.CalculateCost(order.OrderDetails, order.PostalCode);
            }

            var viewModel = new OrderDetailsViewModel
            {
                OrderCostSummary = costSummary,
                Order = order
            };

            return View(viewModel);
        }
    }
}
