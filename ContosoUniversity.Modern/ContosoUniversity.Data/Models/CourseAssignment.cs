using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ContosoUniversity.Data.Models
{
    public class CourseAssignment
    {
        [Key]
        public Guid Id { get; set; }
        
        [Required]
        public Guid InstructorId { get; set; }
        
        [Required]
        public Guid CourseId { get; set; }
        
        // Navigation properties
        public virtual Instructor Instructor { get; set; }
        public virtual Course Course { get; set; }
    }
}
