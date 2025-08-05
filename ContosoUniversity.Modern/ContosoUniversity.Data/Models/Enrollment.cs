using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ContosoUniversity.Data.Models
{
    public enum Grade
    {
        A, B, C, D, F
    }

    public class Enrollment
    {
        [Key]
        public Guid Id { get; set; }
        
        public Guid CourseId { get; set; }
        
        public Guid StudentId { get; set; }
        
        [DisplayFormat(NullDisplayText = "No grade")]
        public Grade? Grade { get; set; }
        
        // Navigation properties
        public virtual Course Course { get; set; }
        public virtual Student Student { get; set; }
    }
}
