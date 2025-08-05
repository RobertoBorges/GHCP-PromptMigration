using ConUniv.Repositories;
using ConUniv.ViewModels;
using DiPS.Client;
using DiPSBackEndApplication.Controller;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ContosoBackend.Controllers
{
    public class Departments : DiPSController
    {

        DepartmentRepository departmentRepository;
        List<string> Errors;
        public Departments(DiPSClient client) : base(client) 
        {
            departmentRepository = new DepartmentRepository();
            Errors = new List<string>();
        }


        public void GetDepartment(dynamic Department)
        {
            DepartmentViewModel model = new DepartmentViewModel();
            model.FillData(Guid.Parse(Department.Id.ToString()));
            DiPSClient.Publish("DepartmentReturned" + Department.Id.ToString(), new { Department = model });
        }

        public void Save(dynamic data)
        {
            try
            {
                DepartmentViewModel model = new DepartmentViewModel();
                model = data.ToObject<DepartmentViewModel>();
                model.Department.Id = model.Department.Id == Guid.Empty ? Guid.NewGuid() : model.Department.Id;
                model.Save();
            }
            catch 
            {
                Errors.Add("Cannot Save the record");
            }
        }

        public void Delete(dynamic Department)
        {
            try
            {
                departmentRepository.Delete(new { Id = Department.Id });
            }
            catch (Exception e)
            {
                Errors.Add("Cannot Delete the record");
            }
            
        }

        public void GetDepartments(dynamic id)
        {
            UpdateDepartments();
        }

        private void UpdateDepartments()
        {
            //return the list of Departments
            DiPSClient.Publish("DepartmentsUpdated", new { Departments = departmentRepository.GetAll(), Errors = Errors });
            Errors.Clear();
        }

    }
}
