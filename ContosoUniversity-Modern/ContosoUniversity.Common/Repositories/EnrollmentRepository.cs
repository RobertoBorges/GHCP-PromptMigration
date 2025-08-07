using ContosoUniversity.Data.DbContexts;
using ContosoUniversity.Data.Entities;
using Microsoft.Extensions.Logging;

namespace ContosoUniversity.Common.Repositories
{
    public class EnrollmentRepository : Repository<Enrollment>, IEnrollmentRepository
    {
        public EnrollmentRepository(ApplicationContext context, ILogger logger) 
            : base(context, logger)
        {
        }
    }
}
