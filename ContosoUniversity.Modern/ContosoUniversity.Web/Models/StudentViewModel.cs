using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace ContosoUniversity.Web.Models
{
    public class StudentViewModel
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
        
        [Display(Name = "Enrollment Date")]
        [DataType(DataType.Date)]
        public DateTime EnrollmentDate { get; set; }
        
        public IEnumerable<EnrollmentViewModel> Enrollments { get; set; } = new List<EnrollmentViewModel>();
    }
}
