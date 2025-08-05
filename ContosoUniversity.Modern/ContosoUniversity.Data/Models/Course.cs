using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ContosoUniversity.Data.Models
{
    public class Course
    {
        [Key]
        public Guid Id { get; set; }
        
        [Required]
        [StringLength(50, MinimumLength = 3)]
        public string Title { get; set; }
        
        [Range(0, 5)]
        public int Credits { get; set; }
        
        public Guid DepartmentId { get; set; }
        
        // Navigation properties
        public virtual Department Department { get; set; }
        public virtual ICollection<Enrollment> Enrollments { get; set; } = new List<Enrollment>();
        public virtual ICollection<CourseAssignment> CourseAssignments { get; set; } = new List<CourseAssignment>();
    }
}
