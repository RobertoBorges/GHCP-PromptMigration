using ContosoUniversity.Data.DbContexts;
using ContosoUniversity.Data.Entities;
using Microsoft.Extensions.Logging;

namespace ContosoUniversity.Common.Repositories
{
    public class StudentRepository : Repository<Student>, IStudentRepository
    {
        public StudentRepository(ApplicationContext context, ILogger logger) 
            : base(context, logger)
        {
        }
    }
}
