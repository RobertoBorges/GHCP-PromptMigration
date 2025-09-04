using System;
using System.ServiceModel;
using WCFDemo.Service;

namespace WCFDemo.Client
{
    /// <summary>
    /// Console application to demonstrate consuming the WCF Customer Service
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            ChannelFactory<ICustomerService> factory = null;
            ICustomerService proxy = null;

            try
            {
                Console.WriteLine("===============================================");
                Console.WriteLine("WCF Demo Client - .NET Framework 3.5");
                Console.WriteLine("===============================================");
                Console.WriteLine();

                // Create a channel factory and proxy to communicate with the service
                var binding = new BasicHttpBinding();
                var address = new EndpointAddress("http://localhost:8080/CustomerService");
                factory = new ChannelFactory<ICustomerService>(binding, address);
                proxy = factory.CreateChannel();

                Console.WriteLine("Connecting to WCF Customer Service...");
                Console.WriteLine();

                // Demonstrate various service operations
                DemonstrateServiceOperations(proxy);
            }
            catch (EndpointNotFoundException)
            {
                Console.WriteLine("ERROR: Could not connect to the WCF service.");
                Console.WriteLine("Make sure the WCFDemo.Host application is running first.");
            }
            catch (Exception ex)
            {
                Console.WriteLine("ERROR: {0}", ex.Message);
                if (ex.InnerException != null)
                {
                    Console.WriteLine("Inner exception: {0}", ex.InnerException.Message);
                }
            }
            finally
            {
                if (proxy != null && proxy is ICommunicationObject)
                {
                    try
                    {
                        ((ICommunicationObject)proxy).Close();
                    }
                    catch
                    {
                        ((ICommunicationObject)proxy).Abort();
                    }
                }

                if (factory != null)
                {
                    try
                    {
                        factory.Close();
                    }
                    catch
                    {
                        factory.Abort();
                    }
                }
            }

            Console.WriteLine();
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }

        /// <summary>
        /// Demonstrates various WCF service operations
        /// </summary>
        /// <param name="proxy">Service proxy</param>
        static void DemonstrateServiceOperations(ICustomerService proxy)
        {
            Console.WriteLine("=== WCF Service Operations Demo ===");
            Console.WriteLine();

            // 1. Get customer count
            Console.WriteLine("1. Getting total customer count...");
            int count = proxy.GetCustomerCount();
            Console.WriteLine("   Total customers: {0}", count);
            Console.WriteLine();

            // 2. Get all customers
            Console.WriteLine("2. Getting all customers...");
            var customers = proxy.GetAllCustomers();
            Console.WriteLine("   Found {0} customers:", customers.Count);
            foreach (var customer in customers)
            {
                Console.WriteLine("   - {0} {1} ({2}) from {3}, {4}", 
                    customer.FirstName, customer.LastName, customer.Email, 
                    customer.City, customer.Country);
            }
            Console.WriteLine();

            // 3. Get customer by ID
            Console.WriteLine("3. Getting customer by ID (ID = 3)...");
            var specificCustomer = proxy.GetCustomerById(3);
            if (specificCustomer != null)
            {
                Console.WriteLine("   Found: {0} {1}, born {2:yyyy-MM-dd}", 
                    specificCustomer.FirstName, specificCustomer.LastName, 
                    specificCustomer.DateOfBirth);
            }
            else
            {
                Console.WriteLine("   Customer not found.");
            }
            Console.WriteLine();

            // 4. Get customers by country
            Console.WriteLine("4. Getting customers from USA...");
            var usaCustomers = proxy.GetCustomersByCountry("USA");
            Console.WriteLine("   Found {0} customers from USA:", usaCustomers.Count);
            foreach (var customer in usaCustomers)
            {
                Console.WriteLine("   - {0} {1} from {2}", 
                    customer.FirstName, customer.LastName, customer.City);
            }
            Console.WriteLine();

            // 5. Add a new customer
            Console.WriteLine("5. Adding a new customer...");
            var newCustomer = new Customer
            {
                FirstName = "Test",
                LastName = "User",
                Email = "test.user@demo.com",
                DateOfBirth = new DateTime(1995, 1, 1),
                City = "Demo City",
                Country = "Demo Country"
            };
            int newId = proxy.AddCustomer(newCustomer);
            Console.WriteLine("   New customer added with ID: {0}", newId);
            Console.WriteLine();

            // 6. Update customer count after addition
            Console.WriteLine("6. Getting updated customer count...");
            count = proxy.GetCustomerCount();
            Console.WriteLine("   Total customers after addition: {0}", count);
            Console.WriteLine();

            // 7. Update the customer
            Console.WriteLine("7. Updating the new customer...");
            newCustomer.Id = newId;
            newCustomer.City = "Updated City";
            bool updateResult = proxy.UpdateCustomer(newCustomer);
            Console.WriteLine("   Update result: {0}", updateResult ? "Success" : "Failed");
            Console.WriteLine();

            // 8. Verify the update
            Console.WriteLine("8. Verifying the update...");
            var updatedCustomer = proxy.GetCustomerById(newId);
            if (updatedCustomer != null)
            {
                Console.WriteLine("   Updated customer: {0} {1} from {2}", 
                    updatedCustomer.FirstName, updatedCustomer.LastName, 
                    updatedCustomer.City);
            }
            Console.WriteLine();

            // 9. Delete the customer
            Console.WriteLine("9. Deleting the test customer...");
            bool deleteResult = proxy.DeleteCustomer(newId);
            Console.WriteLine("   Delete result: {0}", deleteResult ? "Success" : "Failed");
            Console.WriteLine();

            // 10. Final customer count
            Console.WriteLine("10. Final customer count...");
            count = proxy.GetCustomerCount();
            Console.WriteLine("    Total customers after deletion: {0}", count);
            Console.WriteLine();

            Console.WriteLine("=== Demo Complete ===");
        }
    }
}