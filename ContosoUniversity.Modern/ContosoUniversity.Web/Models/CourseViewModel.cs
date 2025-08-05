using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace ContosoUniversity.Web.Models
{
    public class CourseViewModel
    {
        public Guid Id { get; set; }
        
        [Required]
        [StringLength(50, MinimumLength = 3)]
        public string Title { get; set; }
        
        [Range(0, 5)]
        public int Credits { get; set; }
        
        public Guid DepartmentId { get; set; }
        
        public string Department { get; set; }
        
        public IEnumerable<EnrollmentViewModel> Enrollments { get; set; } = new List<EnrollmentViewModel>();
        
        public IEnumerable<InstructorViewModel> Instructors { get; set; } = new List<InstructorViewModel>();
        
        // Property to fix compatibility with views
        public string CourseID => Id.ToString();
    }
}
