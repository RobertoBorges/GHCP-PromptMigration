using ContosoUniversity.Common.Repositories;
using ContosoUniversity.Data.DbContexts;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using System;

namespace ContosoUniversity.Common
{
    public class UnitOfWork : IUnitOfWork
    {
        private readonly ApplicationContext _context;
        private readonly ILogger _logger;

        public IDepartmentRepository Department { get; private set; }
        public ICourseRepository Course { get; private set; }
        public IStudentRepository Student { get; private set; }
        public IInstructorRepository Instructor { get; private set; }
        public IEnrollmentRepository Enrollment { get; private set; }

        public UnitOfWork(ApplicationContext context,
            ILoggerFactory loggerFactory)
        {
            _context = context;
            _logger = loggerFactory.CreateLogger("Contoso University logs");

            Department = new DepartmentRepository(_context, _logger);
            Course = new CourseRepository(_context, _logger);
            Student = new StudentRepository(_context, _logger);
            Instructor = new InstructorRepository(_context, _logger);
            Enrollment = new EnrollmentRepository(_context, _logger);
        }

        public int Complete()
        {
            try
            {
                return _context.SaveChanges();
            }
            catch (DbUpdateConcurrencyException ex)
            {
                _logger.LogError($"DbUpdateConcurrencyException error: {ex.Message}");
                throw;
            }
            catch (DbUpdateException ex)
            {
                _logger.LogError($"DbUpdateException error: {ex.Message}");
                throw;
            }
            catch (Exception ex)
            {
                _logger.LogError($"Complete failed: {ex.Message}");
                throw;
            }
        }

        public void Dispose()
        {
            _context.Dispose();
        }

        public ApplicationContext GetContext()
        {
            return _context;
        }
    }
}
