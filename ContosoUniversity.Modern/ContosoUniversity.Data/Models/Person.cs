using System;
using System.ComponentModel.DataAnnotations;

namespace ContosoUniversity.Data.Models
{
    /// <summary>
    /// Base class for people in the university system
    /// </summary>
    public abstract class Person
    {
        [Key]
        public Guid Id { get; set; }
        
        [Required]
        [StringLength(50)]
        public string LastName { get; set; }
        
        [Required]
        [StringLength(50)]
        public string FirstName { get; set; }
        
        // Calculated property for full name
        public string FullName => $"{FirstName} {LastName}";
    }
}
