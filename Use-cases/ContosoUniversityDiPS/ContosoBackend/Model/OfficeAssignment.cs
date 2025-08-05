using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using Needletail.DataAccess.Attributes;
using DataAccess.Scaffold.Attributes;

namespace ConUniv.Models
{
    public class OfficeAssignment
    {
        
        [Required][TableKey(CanInsertKey = true)]
        public Guid Id { get; set; }
        
        [Required]
        public Guid InstructorID { get; set; }
        
        [MaxLen(50)]
        public string Location { get; set; }
        
    }
}
