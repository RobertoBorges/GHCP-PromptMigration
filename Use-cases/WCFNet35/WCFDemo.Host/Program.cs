using System;
using System.ServiceModel;
using WCFDemo.Service;

namespace WCFDemo.Host
{
    /// <summary>
    /// Console application to host the WCF Customer Service
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            ServiceHost host = null;
            
            try
            {
                Console.WriteLine("===============================================");
                Console.WriteLine("WCF Demo Service Host - .NET Framework 3.5");
                Console.WriteLine("===============================================");
                Console.WriteLine();

                // Create and configure the service host
                host = new ServiceHost(typeof(CustomerService));
                
                Console.WriteLine("Starting WCF Customer Service...");
                host.Open();
                
                Console.WriteLine("Service started successfully!");
                Console.WriteLine();
                Console.WriteLine("Service endpoints:");
                foreach (var endpoint in host.Description.Endpoints)
                {
                    Console.WriteLine("- {0}", endpoint.Address.Uri);
                }
                
                Console.WriteLine();
                Console.WriteLine("Available operations:");
                Console.WriteLine("- GetAllCustomers()");
                Console.WriteLine("- GetCustomerById(int id)");
                Console.WriteLine("- GetCustomersByCountry(string country)");
                Console.WriteLine("- AddCustomer(Customer customer)");
                Console.WriteLine("- UpdateCustomer(Customer customer)");
                Console.WriteLine("- DeleteCustomer(int id)");
                Console.WriteLine("- GetCustomerCount()");
                
                Console.WriteLine();
                Console.WriteLine("The service is ready and running...");
                Console.WriteLine("Press any key to stop the service.");
                Console.ReadKey();
            }
            catch (Exception ex)
            {
                Console.WriteLine();
                Console.WriteLine("Error starting service: {0}", ex.Message);
                if (ex.InnerException != null)
                {
                    Console.WriteLine("Inner exception: {0}", ex.InnerException.Message);
                }
            }
            finally
            {
                if (host != null)
                {
                    try
                    {
                        Console.WriteLine();
                        Console.WriteLine("Stopping service...");
                        host.Close();
                        Console.WriteLine("Service stopped successfully.");
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine("Error stopping service: {0}", ex.Message);
                        host.Abort();
                    }
                }
            }
            
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}