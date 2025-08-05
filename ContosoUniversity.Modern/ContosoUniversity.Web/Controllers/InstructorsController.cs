using AutoMapper;
using ContosoUniversity.Data.Models;
using ContosoUniversity.Data.Repositories;
using ContosoUniversity.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ContosoUniversity.Web.Controllers
{
    public class InstructorsController : BaseController
    {
        private readonly IInstructorRepository _instructorRepository;

        public InstructorsController(
            ILogger<InstructorsController> logger,
            IMapper mapper,
            IInstructorRepository instructorRepository) : base(logger, mapper)
        {
            _instructorRepository = instructorRepository;
        }

        // GET: Instructors
        public async Task<IActionResult> Index()
        {
            var instructors = await _instructorRepository.GetInstructorsWithCoursesAndDepartmentsAsync();
            var viewModel = _mapper.Map<IEnumerable<InstructorViewModel>>(instructors);
            return View(viewModel);
        }

        // GET: Instructors/Details/5
        public async Task<IActionResult> Details(Guid id)
        {
            var instructor = await _instructorRepository.GetInstructorWithCoursesAndDepartmentsAsync(id);
            if (instructor == null)
            {
                return NotFound();
            }

            var viewModel = _mapper.Map<InstructorViewModel>(instructor);
            
            // Ensure department names are correctly mapped
            if (viewModel.Courses != null)
            {
                foreach (var course in viewModel.Courses)
                {
                    if (course.Department == null && !string.IsNullOrEmpty(course.Department))
                    {
                        course.Department = course.Department;
                    }
                }
            }
            
            return View(viewModel);
        }

        // GET: Instructors/Create
        public IActionResult Create()
        {
            return View();
        }

        // POST: Instructors/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(InstructorViewModel instructorVM)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var instructor = _mapper.Map<Instructor>(instructorVM);
                    instructor.Id = Guid.NewGuid(); // Generate new ID
                    
                    // Handle office assignment
                    if (!string.IsNullOrWhiteSpace(instructorVM.OfficeLocation))
                    {
                        instructor.OfficeAssignment = new OfficeAssignment
                        {
                            Id = Guid.NewGuid(),
                            InstructorId = instructor.Id,
                            Location = instructorVM.OfficeLocation
                        };
                    }
                    
                    await _instructorRepository.AddAsync(instructor);
                    await _instructorRepository.SaveChangesAsync();
                    return RedirectToAction(nameof(Index));
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating instructor");
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists, contact your system administrator.");
            }
            
            return View(instructorVM);
        }

        // GET: Instructors/Edit/5
        public async Task<IActionResult> Edit(Guid id)
        {
            var instructor = await _instructorRepository.GetInstructorWithCoursesAndDepartmentsAsync(id);
            if (instructor == null)
            {
                return NotFound();
            }
            
            var viewModel = _mapper.Map<InstructorViewModel>(instructor);
            return View(viewModel);
        }

        // POST: Instructors/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(Guid id, InstructorViewModel instructorVM)
        {
            if (id != instructorVM.Id)
            {
                return NotFound();
            }

            try
            {
                if (ModelState.IsValid)
                {
                    var instructor = await _instructorRepository.GetInstructorWithCoursesAndDepartmentsAsync(id);
                    if (instructor == null)
                    {
                        return NotFound();
                    }

                    _mapper.Map(instructorVM, instructor);
                    
                    // Handle office assignment
                    if (string.IsNullOrWhiteSpace(instructorVM.OfficeLocation))
                    {
                        if (instructor.OfficeAssignment != null)
                        {
                            instructor.OfficeAssignment = null;
                        }
                    }
                    else if (instructor.OfficeAssignment == null)
                    {
                        instructor.OfficeAssignment = new OfficeAssignment
                        {
                            Id = Guid.NewGuid(),
                            InstructorId = instructor.Id,
                            Location = instructorVM.OfficeLocation
                        };
                    }
                    else
                    {
                        instructor.OfficeAssignment.Location = instructorVM.OfficeLocation;
                    }
                    
                    await _instructorRepository.UpdateAsync(instructor);
                    await _instructorRepository.SaveChangesAsync();
                    return RedirectToAction(nameof(Index));
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating instructor");
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists, contact your system administrator.");
            }
            
            return View(instructorVM);
        }

        // GET: Instructors/Delete/5
        public async Task<IActionResult> Delete(Guid id)
        {
            var instructor = await _instructorRepository.GetInstructorWithCoursesAndDepartmentsAsync(id);
            if (instructor == null)
            {
                return NotFound();
            }

            var viewModel = _mapper.Map<InstructorViewModel>(instructor);
            return View(viewModel);
        }

        // POST: Instructors/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(Guid id)
        {
            try
            {
                await _instructorRepository.DeleteAsync(id);
                await _instructorRepository.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting instructor");
                var instructor = await _instructorRepository.GetInstructorWithCoursesAndDepartmentsAsync(id);
                var viewModel = _mapper.Map<InstructorViewModel>(instructor);
                ModelState.AddModelError("", "Unable to delete instructor. Try again, and if the problem persists, contact your system administrator.");
                return View(viewModel);
            }
        }
    }
}
