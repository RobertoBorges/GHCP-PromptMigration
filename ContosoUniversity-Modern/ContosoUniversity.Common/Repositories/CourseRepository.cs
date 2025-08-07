using ContosoUniversity.Data.DbContexts;
using ContosoUniversity.Data.Entities;
using Microsoft.Extensions.Logging;

namespace ContosoUniversity.Common.Repositories
{
    public class CourseRepository : Repository<Course>, ICourseRepository
    {
        public CourseRepository(ApplicationContext context, ILogger logger) 
            : base(context, logger)
        {
        }
    }
}
