using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ContosoUniversity.Data.Models
{
    public class OfficeAssignment
    {
        [Key]
        public Guid Id { get; set; }
        
        [Required]
        public Guid InstructorId { get; set; }
        
        [StringLength(50)]
        public string Location { get; set; }
        
        // Navigation property
        public virtual Instructor Instructor { get; set; }
    }
}
