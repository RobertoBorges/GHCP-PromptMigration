using System;
using System.Collections.Generic;
using System.Text;
using System.Data;
using System.Data.SqlClient;
using BookShop.Common.Models;
using BookShop.DataAccess.Base;

namespace BookShop.DataAccess.Repositories
{
    public class EmployeeRepository : BaseRepository
    {
        public Employee GetEmployeeByWindowsUsername(string windowsUsername)
        {
            string query = @"
                SELECT EmployeeId, FirstName, LastName, Email, Phone, Position, Department,
                       HireDate, Salary, IsActive, IsAdmin, WindowsUsername, CreatedDate, ModifiedDate
                FROM Employees 
                WHERE WindowsUsername = @WindowsUsername AND IsActive = 1";

            SqlParameter[] parameters = { CreateParameter("@WindowsUsername", windowsUsername) };
            DataTable dataTable = ExecuteQuery(query, parameters);
            
            if (dataTable.Rows.Count > 0)
            {
                return ConvertDataRowToEmployee(dataTable.Rows[0]);
            }
            
            return null;
        }

        public List<Employee> GetAllEmployees()
        {
            string query = @"
                SELECT EmployeeId, FirstName, LastName, Email, Phone, Position, Department,
                       HireDate, Salary, IsActive, IsAdmin, WindowsUsername, CreatedDate, ModifiedDate
                FROM Employees 
                WHERE IsActive = 1
                ORDER BY LastName, FirstName";

            DataTable dataTable = ExecuteQuery(query);
            return ConvertDataTableToEmployees(dataTable);
        }

        public Employee GetEmployeeById(int employeeId)
        {
            string query = @"
                SELECT EmployeeId, FirstName, LastName, Email, Phone, Position, Department,
                       HireDate, Salary, IsActive, IsAdmin, WindowsUsername, CreatedDate, ModifiedDate
                FROM Employees 
                WHERE EmployeeId = @EmployeeId";

            SqlParameter[] parameters = { CreateParameter("@EmployeeId", employeeId) };
            DataTable dataTable = ExecuteQuery(query, parameters);
            
            if (dataTable.Rows.Count > 0)
            {
                return ConvertDataRowToEmployee(dataTable.Rows[0]);
            }
            
            return null;
        }

        private Employee ConvertDataRowToEmployee(DataRow row)
        {
            return new Employee
            {
                EmployeeId = Convert.ToInt32(row["EmployeeId"]),
                FirstName = row["FirstName"].ToString(),
                LastName = row["LastName"].ToString(),
                Email = row["Email"].ToString(),
                Phone = row["Phone"].ToString(),
                Position = row["Position"].ToString(),
                Department = row["Department"].ToString(),
                HireDate = Convert.ToDateTime(row["HireDate"]),
                Salary = Convert.ToDecimal(row["Salary"]),
                IsActive = Convert.ToBoolean(row["IsActive"]),
                IsAdmin = Convert.ToBoolean(row["IsAdmin"]),
                WindowsUsername = row["WindowsUsername"].ToString(),
                CreatedDate = Convert.ToDateTime(row["CreatedDate"]),
                ModifiedDate = Convert.ToDateTime(row["ModifiedDate"])
            };
        }

        private List<Employee> ConvertDataTableToEmployees(DataTable dataTable)
        {
            List<Employee> employees = new List<Employee>();

            foreach (DataRow row in dataTable.Rows)
            {
                employees.Add(ConvertDataRowToEmployee(row));
            }

            return employees;
        }
    }
}