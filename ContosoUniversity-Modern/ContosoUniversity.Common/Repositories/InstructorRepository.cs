using ContosoUniversity.Data.DbContexts;
using ContosoUniversity.Data.Entities;
using Microsoft.Extensions.Logging;

namespace ContosoUniversity.Common.Repositories
{
    public class InstructorRepository : Repository<Instructor>, IInstructorRepository
    {
        public InstructorRepository(ApplicationContext context, ILogger logger) 
            : base(context, logger)
        {
        }
    }
}
