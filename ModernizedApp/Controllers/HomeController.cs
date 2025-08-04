using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using ASPStoreModernized.Models;

namespace ASPStoreModernized.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;

    public HomeController(ILogger<HomeController> logger)
    {
        _logger = logger;
    }

    public IActionResult Index()
    {
        return View();
    }

    public IActionResult About()
    {
        return View();
    }

    public IActionResult Contact()
    {
        return View();
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult Contact(ContactForm contactForm)
    {
        if (!ModelState.IsValid)
        {
            return View(contactForm);
        }

        // In a real application, we would save this to a database or send an email
        // For this demo, we'll just show a success message
        TempData["SuccessMessage"] = "Thank you for your message! We'll get back to you soon.";
        
        return RedirectToAction(nameof(Contact));
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}
