using System;
using System.Collections.Generic;
using System.Text;

namespace BookShop.Common.Models
{
    public class Author
    {
        public int AuthorId { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Biography { get; set; }
        public DateTime? BirthDate { get; set; }
        public string Nationality { get; set; }
        public string PhotoUrl { get; set; }
        public bool IsActive { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime ModifiedDate { get; set; }
        
        public string FullName
        {
            get { return FirstName + " " + LastName; }
        }
    }
}