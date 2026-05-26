using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using PartsUnlimited.Models;

namespace PartsUnlimited.Utils
{
    public class RaincheckQuery : IRaincheckQuery
    {
        private readonly IPartsUnlimitedContext context;

        public RaincheckQuery(IPartsUnlimitedContext context)
        {
            this.context = context;
        }

        public async Task<IEnumerable<Raincheck>> GetAllAsync()
        {
            var rainchecks = await context.RainChecks.ToListAsync();
            foreach (var raincheck in rainchecks)
            {
                await FillRaincheckValuesAsync(raincheck);
            }
            return rainchecks;
        }

        public async Task<Raincheck> FindAsync(int id)
        {
            var raincheck = await context.RainChecks.FirstOrDefaultAsync(r => r.RaincheckId == id);
            if (raincheck == null)
            {
                throw new ArgumentOutOfRangeException(nameof(id));
            }
            await FillRaincheckValuesAsync(raincheck);
            return raincheck;
        }

        public async Task<int> AddAsync(Raincheck raincheck)
        {
            context.RainChecks.Add(raincheck);
            await context.SaveChangesAsync(CancellationToken.None);
            return raincheck.RaincheckId;
        }

        private async Task FillRaincheckValuesAsync(Raincheck raincheck)
        {
            raincheck.IssuerStore = await context.Stores.FirstAsync(s => s.StoreId == raincheck.StoreId);
            raincheck.Product = await context.Products.FirstAsync(p => p.ProductId == raincheck.ProductId);
            raincheck.Product.Category = await context.Categories.FirstAsync(c => c.CategoryId == raincheck.Product.CategoryId);
        }
    }
}
