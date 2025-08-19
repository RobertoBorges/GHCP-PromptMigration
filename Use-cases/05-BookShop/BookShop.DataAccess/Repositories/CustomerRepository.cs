using System;
using System.Collections.Generic;
using System.Text;
using BookShop.Common.Models;
using BookShop.DataAccess.Base;

namespace BookShop.DataAccess.Repositories
{
    public class CustomerRepository : BaseRepository
    {
        // Basic customer repository for future expansion
        public bool InsertCustomer(Customer customer)
        {
            string query = @"
                INSERT INTO Customers (FirstName, LastName, Email, Phone, Address, City, State, ZipCode, Country, IsActive, CreatedDate, ModifiedDate)
                VALUES (@FirstName, @LastName, @Email, @Phone, @Address, @City, @State, @ZipCode, @Country, @IsActive, @CreatedDate, @ModifiedDate)";

            var parameters = new[] {
                CreateParameter("@FirstName", customer.FirstName),
                CreateParameter("@LastName", customer.LastName),
                CreateParameter("@Email", customer.Email),
                CreateParameter("@Phone", customer.Phone),
                CreateParameter("@Address", customer.Address),
                CreateParameter("@City", customer.City),
                CreateParameter("@State", customer.State),
                CreateParameter("@ZipCode", customer.ZipCode),
                CreateParameter("@Country", customer.Country),
                CreateParameter("@IsActive", true),
                CreateParameter("@CreatedDate", DateTime.Now),
                CreateParameter("@ModifiedDate", DateTime.Now)
            };

            return ExecuteNonQuery(query, parameters) > 0;
        }
    }
}