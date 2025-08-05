using System;
using System.ComponentModel.DataAnnotations;

namespace ContosoUniversity.Web.Models
{
    public enum Grade
    {
        A, B, C, D, F
    }

    public class EnrollmentViewModel
    {
        public Guid Id { get; set; }
        
        public Guid CourseId { get; set; }
        
        public Guid StudentId { get; set; }
        
        [DisplayFormat(NullDisplayText = "No grade")]
        public Grade? Grade { get; set; }
        
        public CourseViewModel Course { get; set; }
        public StudentViewModel Student { get; set; }
    }
}
