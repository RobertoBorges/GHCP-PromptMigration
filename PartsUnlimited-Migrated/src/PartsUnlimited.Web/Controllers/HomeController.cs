using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Memory;
using PartsUnlimited.Models;
using PartsUnlimited.ViewModels;

namespace PartsUnlimited.Controllers
{
    public class HomeController : Controller
    {
        private readonly IPartsUnlimitedContext _db;
        private readonly IMemoryCache _cache;

        public HomeController(IPartsUnlimitedContext context, IMemoryCache cache)
        {
            _db = context;
            _cache = cache;
        }

        public IActionResult Index()
        {
            if (!_cache.TryGetValue<List<Product>>("topselling", out var topSellingProducts))
            {
                topSellingProducts = GetTopSellingProducts(4);
                _cache.Set("topselling", topSellingProducts, TimeSpan.FromMinutes(10));
            }

            if (!_cache.TryGetValue<List<Product>>("newarrivals", out var newProducts))
            {
                newProducts = GetNewProducts(4);
                _cache.Set("newarrivals", newProducts, TimeSpan.FromMinutes(10));
            }

            var viewModel = new HomeViewModel
            {
                NewProducts = newProducts,
                TopSellingProducts = topSellingProducts,
                CommunityPosts = GetCommunityPosts()
            };

            return View(viewModel);
        }

        private List<Product> GetTopSellingProducts(int count)
        {
            return _db.Products
                .OrderByDescending(a => a.OrderDetails.Count())
                .Take(count)
                .ToList();
        }

        private List<Product> GetNewProducts(int count)
        {
            return _db.Products
                .OrderByDescending(a => a.Created)
                .Take(count)
                .ToList();
        }

        private List<CommunityPost> GetCommunityPosts()
        {
            return new List<CommunityPost>
            {
                new CommunityPost { Content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus commodo tellus lorem, et bibendum velit sagittis in. Integer nisl augue, cursus id tellus in, sodales porta.", DatePosted = DateTime.Now, Image = "community_1.png", Source = CommunitySource.Facebook },
                new CommunityPost { Content = " Donec tincidunt risus in ligula varius, feugiat placerat nisi condimentum. Quisque rutrum eleifend venenatis. Phasellus a hendrerit urna. Cras arcu leo, hendrerit vel mollis nec.", DatePosted = DateTime.Now, Image = "community_2.png", Source = CommunitySource.Facebook },
                new CommunityPost { Content = "Aenean vestibulum non lacus non molestie. Curabitur maximus interdum magna, ullamcorper facilisis tellus fermentum eu. Pellentesque iaculis enim ac vestibulum mollis.", DatePosted = DateTime.Now, Image = "community_3.png", Source = CommunitySource.Facebook },
                new CommunityPost { Content = "Ut consectetur sed justo vel convallis. Vestibulum quis metus leo. Nulla hendrerit pharetra dui, vel euismod lectus elementum sit amet. Nam dolor turpis, sodales non mi nec.", DatePosted = DateTime.Now, Image = "community_4.png", Source = CommunitySource.Facebook }
            };
        }
    }
}
