using AutoMapper;
using ContosoUniversity.Data.Models;
using ContosoUniversity.Data.Repositories;
using ContosoUniversity.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ContosoUniversity.Web.Controllers
{
    public class CoursesController : BaseController
    {
        private readonly ICourseRepository _courseRepository;
        private readonly IDepartmentRepository _departmentRepository;

        public CoursesController(
            ILogger<CoursesController> logger,
            IMapper mapper,
            ICourseRepository courseRepository,
            IDepartmentRepository departmentRepository) : base(logger, mapper)
        {
            _courseRepository = courseRepository;
            _departmentRepository = departmentRepository;
        }

        // GET: Courses
        public async Task<IActionResult> Index()
        {
            var courses = await _courseRepository.GetCoursesWithDepartmentAsync();
            var viewModel = _mapper.Map<IEnumerable<CourseViewModel>>(courses);
            return View(viewModel);
        }

        // GET: Courses/Details/5
        public async Task<IActionResult> Details(Guid id)
        {
            var course = await _courseRepository.GetCourseWithDetailsAsync(id);
            if (course == null)
            {
                return NotFound();
            }

            var viewModel = _mapper.Map<CourseViewModel>(course);
            return View(viewModel);
        }

        // GET: Courses/Create
        public async Task<IActionResult> Create()
        {
            var departments = await _departmentRepository.GetAllAsync();
            ViewData["DepartmentId"] = new SelectList(departments, "Id", "Name");
            return View();
        }

        // POST: Courses/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(CourseViewModel courseVM)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var course = _mapper.Map<Course>(courseVM);
                    course.Id = Guid.NewGuid(); // Generate new ID
                    await _courseRepository.AddAsync(course);
                    await _courseRepository.SaveChangesAsync();
                    return RedirectToAction(nameof(Index));
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating course");
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists, contact your system administrator.");
            }
            
            var departments = await _departmentRepository.GetAllAsync();
            ViewData["DepartmentId"] = new SelectList(departments, "Id", "Name", courseVM.DepartmentId);
            return View(courseVM);
        }

        // GET: Courses/Edit/5
        public async Task<IActionResult> Edit(Guid id)
        {
            var course = await _courseRepository.GetByIdAsync(id);
            if (course == null)
            {
                return NotFound();
            }
            
            var departments = await _departmentRepository.GetAllAsync();
            ViewData["DepartmentId"] = new SelectList(departments, "Id", "Name", course.DepartmentId);
            var viewModel = _mapper.Map<CourseViewModel>(course);
            return View(viewModel);
        }

        // POST: Courses/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(Guid id, CourseViewModel courseVM)
        {
            if (id != courseVM.Id)
            {
                return NotFound();
            }

            try
            {
                if (ModelState.IsValid)
                {
                    var course = await _courseRepository.GetByIdAsync(id);
                    if (course == null)
                    {
                        return NotFound();
                    }

                    _mapper.Map(courseVM, course);
                    await _courseRepository.UpdateAsync(course);
                    await _courseRepository.SaveChangesAsync();
                    return RedirectToAction(nameof(Index));
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating course");
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists, contact your system administrator.");
            }
            
            var departments = await _departmentRepository.GetAllAsync();
            ViewData["DepartmentId"] = new SelectList(departments, "Id", "Name", courseVM.DepartmentId);
            return View(courseVM);
        }

        // GET: Courses/Delete/5
        public async Task<IActionResult> Delete(Guid id)
        {
            var course = await _courseRepository.GetCourseWithDetailsAsync(id);
            if (course == null)
            {
                return NotFound();
            }

            var viewModel = _mapper.Map<CourseViewModel>(course);
            return View(viewModel);
        }

        // POST: Courses/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(Guid id)
        {
            try
            {
                await _courseRepository.DeleteAsync(id);
                await _courseRepository.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting course");
                var course = await _courseRepository.GetCourseWithDetailsAsync(id);
                var viewModel = _mapper.Map<CourseViewModel>(course);
                ModelState.AddModelError("", "Unable to delete course. Try again, and if the problem persists, contact your system administrator.");
                return View(viewModel);
            }
        }
    }
}
