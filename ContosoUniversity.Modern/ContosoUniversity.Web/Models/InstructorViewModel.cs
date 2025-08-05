using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace ContosoUniversity.Web.Models
{
    public class InstructorViewModel
    {
        public Guid Id { get; set; }
        
        [Display(Name = "Last Name")]
        [Required]
        [StringLength(50)]
        public string LastName { get; set; }
        
        [Display(Name = "First Name")]
        [Required]
        [StringLength(50)]
        public string FirstName { get; set; }
        
        [Display(Name = "Full Name")]
        public string FullName => $"{FirstName} {LastName}";
        
        [Display(Name = "Hire Date")]
        [DataType(DataType.Date)]
        public DateTime HireDate { get; set; }
        
        [Display(Name = "Office Location")]
        public string OfficeLocation { get; set; }
        
        public IEnumerable<CourseViewModel> Courses { get; set; } = new List<CourseViewModel>();
        
        public IEnumerable<CourseViewModel> AssignedCourses => Courses;
    }
}
