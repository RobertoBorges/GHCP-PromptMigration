using System;
using System.Collections.Generic;
using System.Text;

namespace BookShop.Common.Models
{
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Email { get; set; }
        public string Phone { get; set; }
        public string Position { get; set; }
        public string Department { get; set; }
        public DateTime HireDate { get; set; }
        public decimal Salary { get; set; }
        public bool IsActive { get; set; }
        public bool IsAdmin { get; set; }
        public string WindowsUsername { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime ModifiedDate { get; set; }
        
        public string FullName
        {
            get { return FirstName + " " + LastName; }
        }
    }
}