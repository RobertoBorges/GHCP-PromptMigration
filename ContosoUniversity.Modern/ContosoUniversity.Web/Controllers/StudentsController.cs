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
    public class StudentsController : BaseController
    {
        private readonly IStudentRepository _studentRepository;

        public StudentsController(
            ILogger<StudentsController> logger,
            IMapper mapper,
            IStudentRepository studentRepository) : base(logger, mapper)
        {
            _studentRepository = studentRepository;
        }

        // GET: Students
        public async Task<IActionResult> Index()
        {
            var students = await _studentRepository.GetAllAsync();
            var viewModel = _mapper.Map<IEnumerable<StudentViewModel>>(students);
            return View(viewModel);
        }

        // GET: Students/Details/5
        public async Task<IActionResult> Details(Guid id)
        {
            var student = await _studentRepository.GetStudentWithEnrollmentsAsync(id);
            if (student == null)
            {
                return NotFound();
            }

            var viewModel = _mapper.Map<StudentViewModel>(student);
            return View(viewModel);
        }

        // GET: Students/Create
        public IActionResult Create()
        {
            return View();
        }

        // POST: Students/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(StudentViewModel studentVM)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var student = _mapper.Map<Student>(studentVM);
                    student.Id = Guid.NewGuid(); // Generate new ID
                    await _studentRepository.AddAsync(student);
                    await _studentRepository.SaveChangesAsync();
                    return RedirectToAction(nameof(Index));
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating student");
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists, contact your system administrator.");
            }
            
            return View(studentVM);
        }

        // GET: Students/Edit/5
        public async Task<IActionResult> Edit(Guid id)
        {
            var student = await _studentRepository.GetByIdAsync(id);
            if (student == null)
            {
                return NotFound();
            }
            
            var viewModel = _mapper.Map<StudentViewModel>(student);
            return View(viewModel);
        }

        // POST: Students/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(Guid id, StudentViewModel studentVM)
        {
            if (id != studentVM.Id)
            {
                return NotFound();
            }

            try
            {
                if (ModelState.IsValid)
                {
                    var student = await _studentRepository.GetByIdAsync(id);
                    if (student == null)
                    {
                        return NotFound();
                    }

                    _mapper.Map(studentVM, student);
                    await _studentRepository.UpdateAsync(student);
                    await _studentRepository.SaveChangesAsync();
                    return RedirectToAction(nameof(Index));
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating student");
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists, contact your system administrator.");
            }
            
            return View(studentVM);
        }

        // GET: Students/Delete/5
        public async Task<IActionResult> Delete(Guid id)
        {
            var student = await _studentRepository.GetStudentWithEnrollmentsAsync(id);
            if (student == null)
            {
                return NotFound();
            }

            var viewModel = _mapper.Map<StudentViewModel>(student);
            return View(viewModel);
        }

        // POST: Students/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(Guid id)
        {
            try
            {
                await _studentRepository.DeleteAsync(id);
                await _studentRepository.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting student");
                var student = await _studentRepository.GetStudentWithEnrollmentsAsync(id);
                var viewModel = _mapper.Map<StudentViewModel>(student);
                ModelState.AddModelError("", "Unable to delete student. Try again, and if the problem persists, contact your system administrator.");
                return View(viewModel);
            }
        }
    }
}
