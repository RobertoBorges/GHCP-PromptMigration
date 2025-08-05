using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using Needletail.DataAccess.Attributes;
using DataAccess.Scaffold.Attributes;

namespace ConUniv.Models
{
    public class Person
    {
        
        [Required][TableKey(CanInsertKey = true)]
        public Guid Id { get; set; }
        
        [Required][MaxLen(50)]
        public string LastName { get; set; }
        
        [Required][MaxLen(50)]
        public string FirstName { get; set; }
        
        
        public DateTime HireDate { get; set; }
        
        
        public DateTime EnrollmentDate { get; set; }
        
        [Required][MaxLen(128)]
        public string Discriminator { get; set; }
        
    }
}
