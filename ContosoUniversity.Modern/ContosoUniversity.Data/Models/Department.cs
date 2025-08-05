using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ContosoUniversity.Data.Models
{
    public class Department
    {
        [Key]
        public Guid Id { get; set; }
        
        [Required]
        [StringLength(50, MinimumLength = 3)]
        public string Name { get; set; }
        
        [DataType(DataType.Currency)]
        [Column(TypeName = "money")]
        public decimal Budget { get; set; }
        
        [DataType(DataType.Date)]
        [DisplayFormat(DataFormatString = "{0:yyyy-MM-dd}", ApplyFormatInEditMode = true)]
        public DateTime StartDate { get; set; }
        
        // Foreign key
        public Guid? InstructorId { get; set; }
        
        // Navigation properties
        public virtual Instructor Administrator { get; set; }
        public virtual ICollection<Course> Courses { get; set; } = new List<Course>();
    }
}
