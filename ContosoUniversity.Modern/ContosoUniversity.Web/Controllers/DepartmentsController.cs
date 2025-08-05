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
    public class DepartmentsController : BaseController
    {
        private readonly IDepartmentRepository _departmentRepository;
        private readonly IInstructorRepository _instructorRepository;

        public DepartmentsController(
            ILogger<DepartmentsController> logger,
            IMapper mapper,
            IDepartmentRepository departmentRepository,
            IInstructorRepository instructorRepository) : base(logger, mapper)
        {
            _departmentRepository = departmentRepository;
            _instructorRepository = instructorRepository;
        }

        // GET: Departments
        public async Task<IActionResult> Index()
        {
            var departments = await _departmentRepository.GetDepartmentsWithAdministratorAsync();
            var viewModel = _mapper.Map<IEnumerable<DepartmentViewModel>>(departments);
            return View(viewModel);
        }

        // GET: Departments/Details/5
        public async Task<IActionResult> Details(Guid id)
        {
            var department = await _departmentRepository.GetDepartmentWithDetailsAsync(id);
            if (department == null)
            {
                return NotFound();
            }

            var viewModel = _mapper.Map<DepartmentViewModel>(department);
            return View(viewModel);
        }

        // GET: Departments/Create
        public async Task<IActionResult> Create()
        {
            var instructors = await _instructorRepository.GetAllAsync();
            ViewData["InstructorId"] = new SelectList(instructors, "Id", "FullName");
            return View();
        }

        // POST: Departments/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(DepartmentViewModel departmentVM)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var department = _mapper.Map<Department>(departmentVM);
                    department.Id = Guid.NewGuid(); // Generate new ID
                    await _departmentRepository.AddAsync(department);
                    await _departmentRepository.SaveChangesAsync();
                    return RedirectToAction(nameof(Index));
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating department");
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists, contact your system administrator.");
            }
            
            var instructors = await _instructorRepository.GetAllAsync();
            ViewData["InstructorId"] = new SelectList(instructors, "Id", "FullName", departmentVM.InstructorId);
            return View(departmentVM);
        }

        // GET: Departments/Edit/5
        public async Task<IActionResult> Edit(Guid id)
        {
            var department = await _departmentRepository.GetByIdAsync(id);
            if (department == null)
            {
                return NotFound();
            }
            
            var instructors = await _instructorRepository.GetAllAsync();
            ViewData["InstructorId"] = new SelectList(instructors, "Id", "FullName", department.InstructorId);
            var viewModel = _mapper.Map<DepartmentViewModel>(department);
            return View(viewModel);
        }

        // POST: Departments/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(Guid id, DepartmentViewModel departmentVM)
        {
            if (id != departmentVM.Id)
            {
                return NotFound();
            }

            try
            {
                if (ModelState.IsValid)
                {
                    var department = await _departmentRepository.GetByIdAsync(id);
                    if (department == null)
                    {
                        return NotFound();
                    }

                    _mapper.Map(departmentVM, department);
                    await _departmentRepository.UpdateAsync(department);
                    await _departmentRepository.SaveChangesAsync();
                    return RedirectToAction(nameof(Index));
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating department");
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists, contact your system administrator.");
            }
            
            var instructors = await _instructorRepository.GetAllAsync();
            ViewData["InstructorId"] = new SelectList(instructors, "Id", "FullName", departmentVM.InstructorId);
            return View(departmentVM);
        }

        // GET: Departments/Delete/5
        public async Task<IActionResult> Delete(Guid id)
        {
            var department = await _departmentRepository.GetDepartmentWithDetailsAsync(id);
            if (department == null)
            {
                return NotFound();
            }

            var viewModel = _mapper.Map<DepartmentViewModel>(department);
            return View(viewModel);
        }

        // POST: Departments/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(Guid id)
        {
            try
            {
                await _departmentRepository.DeleteAsync(id);
                await _departmentRepository.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting department");
                var department = await _departmentRepository.GetDepartmentWithDetailsAsync(id);
                var viewModel = _mapper.Map<DepartmentViewModel>(department);
                ModelState.AddModelError("", "Unable to delete department. Try again, and if the problem persists, contact your system administrator.");
                return View(viewModel);
            }
        }
    }
}
