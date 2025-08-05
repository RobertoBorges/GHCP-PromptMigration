using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ContosoUniversity.Web.Models
{
    public class DepartmentViewModel
    {
        public Guid Id { get; set; }
        
        [Required]
        [StringLength(50, MinimumLength = 3)]
        public string Name { get; set; }
        
        [DataType(DataType.Currency)]
        [Range(0, 1000000)]
        public decimal Budget { get; set; }
        
        [DataType(DataType.Date)]
        [DisplayFormat(DataFormatString = "{0:yyyy-MM-dd}", ApplyFormatInEditMode = true)]
        [Display(Name = "Start Date")]
        public DateTime StartDate { get; set; }
        
        public Guid? InstructorId { get; set; }
        
        [Display(Name = "Administrator")]
        public string AdministratorName { get; set; }
        
        public IEnumerable<CourseViewModel> Courses { get; set; } = new List<CourseViewModel>();
    }
}
