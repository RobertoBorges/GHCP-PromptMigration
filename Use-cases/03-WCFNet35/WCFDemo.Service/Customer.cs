using System;
using System.Runtime.Serialization;

namespace WCFDemo.Service
{
    /// <summary>
    /// Data contract representing a customer entity
    /// </summary>
    [DataContract]
    public class Customer
    {
        [DataMember]
        public int Id { get; set; }

        [DataMember]
        public string FirstName { get; set; }

        [DataMember]
        public string LastName { get; set; }

        [DataMember]
        public string Email { get; set; }

        [DataMember]
        public DateTime DateOfBirth { get; set; }

        [DataMember]
        public string City { get; set; }

        [DataMember]
        public string Country { get; set; }

        [DataMember]
        public bool IsActive { get; set; }

        public Customer()
        {
            IsActive = true;
        }

        public Customer(int id, string firstName, string lastName, string email, DateTime dateOfBirth, string city, string country)
        {
            Id = id;
            FirstName = firstName;
            LastName = lastName;
            Email = email;
            DateOfBirth = dateOfBirth;
            City = city;
            Country = country;
            IsActive = true;
        }
    }
}