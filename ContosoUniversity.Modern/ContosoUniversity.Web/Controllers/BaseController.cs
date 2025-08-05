using AutoMapper;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace ContosoUniversity.Web.Controllers
{
    [AllowAnonymous] // We will modify this later to require authentication
    public abstract class BaseController : Controller
    {
        protected readonly ILogger _logger;
        protected readonly IMapper _mapper;

        protected BaseController(ILogger logger, IMapper mapper)
        {
            _logger = logger;
            _mapper = mapper;
        }
    }
}
