using ContosoUniversity.Data.DbContexts;
using ContosoUniversity.Data.Entities;
using Microsoft.Extensions.Logging;

namespace ContosoUniversity.Common.Repositories
{
    public class DepartmentRepository : Repository<Department>, IDepartmentRepository
    {
        public DepartmentRepository(ApplicationContext context, ILogger logger) 
            : base(context, logger)
        {
        }
    }
}
