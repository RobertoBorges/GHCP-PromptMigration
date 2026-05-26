using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using PartsUnlimited.Models;
using PartsUnlimited.Utils;

namespace PartsUnlimited.Api
{
    [ApiController]
    [Route("api/raincheck")]
    public class RaincheckController : ControllerBase
    {
        private readonly IRaincheckQuery _query;

        public RaincheckController(IRaincheckQuery query)
        {
            _query = query;
        }

        [HttpGet]
        public Task<IEnumerable<Raincheck>> Get()
        {
            return _query.GetAllAsync();
        }

        [HttpGet("{id}")]
        public Task<Raincheck> Get(int id)
        {
            return _query.FindAsync(id);
        }

        [HttpPost]
        public Task<int> Post([FromBody] Raincheck raincheck)
        {
            return _query.AddAsync(raincheck);
        }
    }
}
