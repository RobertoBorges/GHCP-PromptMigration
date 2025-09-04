using System;
using System.Collections.Generic;
using System.Text;
using BookShop.Common.Models;
using BookShop.DataAccess.Repositories;

namespace BookShop.BusinessLogic.Services
{
    public class EmployeeService
    {
        private readonly EmployeeRepository _employeeRepository;

        public EmployeeService()
        {
            _employeeRepository = new EmployeeRepository();
        }

        public Employee AuthenticateEmployee(string windowsUsername)
        {
            if (string.IsNullOrEmpty(windowsUsername))
                throw new ArgumentException("Windows username is required", "windowsUsername");

            try
            {
                return _employeeRepository.GetEmployeeByWindowsUsername(windowsUsername);
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error authenticating employee: " + ex.Message, ex);
            }
        }

        public bool IsEmployeeAdmin(string windowsUsername)
        {
            try
            {
                Employee employee = _employeeRepository.GetEmployeeByWindowsUsername(windowsUsername);
                return employee != null && employee.IsAdmin;
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error checking admin status: " + ex.Message, ex);
            }
        }

        public List<Employee> GetAllEmployees()
        {
            try
            {
                return _employeeRepository.GetAllEmployees();
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error retrieving employees: " + ex.Message, ex);
            }
        }
    }
}