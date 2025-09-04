using System;
using System.Collections.Generic;
using System.ServiceModel;

namespace WCFDemo.Service
{
    /// <summary>
    /// WCF Service Contract for customer operations
    /// </summary>
    [ServiceContract]
    public interface ICustomerService
    {
        /// <summary>
        /// Gets all customers
        /// </summary>
        /// <returns>List of all customers</returns>
        [OperationContract]
        List<Customer> GetAllCustomers();

        /// <summary>
        /// Gets a customer by ID
        /// </summary>
        /// <param name="customerId">The customer ID</param>
        /// <returns>Customer object if found, null otherwise</returns>
        [OperationContract]
        Customer GetCustomerById(int customerId);

        /// <summary>
        /// Gets customers by country
        /// </summary>
        /// <param name="country">The country name</param>
        /// <returns>List of customers from the specified country</returns>
        [OperationContract]
        List<Customer> GetCustomersByCountry(string country);

        /// <summary>
        /// Adds a new customer
        /// </summary>
        /// <param name="customer">The customer to add</param>
        /// <returns>The ID of the newly created customer</returns>
        [OperationContract]
        int AddCustomer(Customer customer);

        /// <summary>
        /// Updates an existing customer
        /// </summary>
        /// <param name="customer">The customer with updated information</param>
        /// <returns>True if update was successful, false otherwise</returns>
        [OperationContract]
        bool UpdateCustomer(Customer customer);

        /// <summary>
        /// Deletes a customer by ID
        /// </summary>
        /// <param name="customerId">The customer ID to delete</param>
        /// <returns>True if deletion was successful, false otherwise</returns>
        [OperationContract]
        bool DeleteCustomer(int customerId);

        /// <summary>
        /// Gets the total number of customers
        /// </summary>
        /// <returns>Total customer count</returns>
        [OperationContract]
        int GetCustomerCount();
    }
}