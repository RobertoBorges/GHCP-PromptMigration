using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using ContosoUniversity.Web.Models;
using AutoMapper;
using ContosoUniversity.Data.Repositories;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.ApplicationInsights;
using Microsoft.AspNetCore.Authorization;

namespace ContosoUniversity.Web.Controllers;

[AllowAnonymous]
public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;
    private readonly IMapper _mapper;
    private readonly IStudentRepository _studentRepository;
    private readonly ICourseRepository _courseRepository;
    private readonly TelemetryClient _telemetryClient;

    public HomeController(
        ILogger<HomeController> logger,
        IMapper mapper,
        IStudentRepository studentRepository,
        ICourseRepository courseRepository,
        TelemetryClient telemetryClient)
    {
        _logger = logger;
        _mapper = mapper;
        _studentRepository = studentRepository;
        _courseRepository = courseRepository;
        _telemetryClient = telemetryClient;
    }

    public async Task<IActionResult> Index()
    {
        _logger.LogInformation("Home page visited");
        _telemetryClient.TrackEvent("HomePageVisit");

        var students = await _studentRepository.GetAllAsync();
        var courses = await _courseRepository.GetAllAsync();
        
        var viewModel = new HomeViewModel
        {
            StudentCount = students.Count(),
            CourseCount = courses.Count()
        };
        
        return View(viewModel);
    }

    public IActionResult Privacy()
    {
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
    
    public IActionResult About()
    {
        return View();
    }
}
