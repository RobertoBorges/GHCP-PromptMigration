using AutoMapper;
using ContosoUniversity.Data.Models;
using ContosoUniversity.Web.Models;
using System.Linq;

namespace ContosoUniversity.Web.Mapping
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            // Student mappings
            CreateMap<Student, StudentViewModel>();
            CreateMap<StudentViewModel, Student>();
            
            // Course mappings
            CreateMap<Course, CourseViewModel>()
                .ForMember(dest => dest.Department, opt => opt.MapFrom(src => 
                    src.Department != null ? src.Department.Name : string.Empty));
            CreateMap<CourseViewModel, Course>();
            
            // Instructor mappings
            CreateMap<Instructor, InstructorViewModel>()
                .ForMember(dest => dest.OfficeLocation, opt => opt.MapFrom(src => 
                    src.OfficeAssignment != null ? src.OfficeAssignment.Location : null))
                .ForMember(dest => dest.Courses, opt => opt.MapFrom(src => 
                    src.CourseAssignments.Select(ca => ca.Course)));
            CreateMap<InstructorViewModel, Instructor>();
            
            // Department mappings
            CreateMap<Department, DepartmentViewModel>()
                .ForMember(dest => dest.AdministratorName, opt => opt.MapFrom(src => 
                    src.Administrator != null ? $"{src.Administrator.FirstName} {src.Administrator.LastName}" : string.Empty));
            CreateMap<DepartmentViewModel, Department>();
            
            // Enrollment mappings
            CreateMap<Enrollment, EnrollmentViewModel>();
            CreateMap<EnrollmentViewModel, Enrollment>();
            
            // Convert between Data and Web enums
            CreateMap<Data.Models.Grade?, Web.Models.Grade?>().ConvertUsing(src => src.HasValue ? (Web.Models.Grade)src.Value : null);
            CreateMap<Web.Models.Grade?, Data.Models.Grade?>().ConvertUsing(src => src.HasValue ? (Data.Models.Grade)src.Value : null);
        }
    }
}
