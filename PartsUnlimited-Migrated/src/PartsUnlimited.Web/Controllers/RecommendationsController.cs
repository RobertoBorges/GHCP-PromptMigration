using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using PartsUnlimited.Models;
using PartsUnlimited.Recommendations;

namespace PartsUnlimited.Controllers
{
    public class RecommendationsController : Controller
    {
        private readonly IPartsUnlimitedContext db;
        private readonly IRecommendationEngine recommendation;
        private readonly IConfiguration _configuration;

        public RecommendationsController(IPartsUnlimitedContext context, IRecommendationEngine recommendationEngine, IConfiguration configuration)
        {
            db = context;
            recommendation = recommendationEngine;
            _configuration = configuration;
        }

        public async Task<IActionResult> GetRecommendations(string productId)
        {
            if (!_configuration.GetValue<bool>("AppSettings:ShowRecommendations"))
            {
                return new EmptyResult();
            }

            var recommendedProductIds = await recommendation.GetRecommendationsAsync(productId);
            var recommendedProducts = await db.Products
                .Where(x => recommendedProductIds.Contains(x.ProductId.ToString()))
                .ToListAsync();

            return PartialView("_Recommendations", recommendedProducts);
        }
    }
}
