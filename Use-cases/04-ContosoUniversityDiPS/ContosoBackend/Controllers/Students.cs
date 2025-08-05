using ConUniv.Models;
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
    public class Students : DiPSController
    {

        StudentRepository sRepo;
        List<string> Errors;

        public Students(DiPSClient client) : base(client) 
        {
            sRepo = new StudentRepository();
            Errors = new List<string>();
        }



        public void GetStudent(dynamic Student)
        {
            StudentViewModel model = new StudentViewModel();
            model.FillData(Guid.Parse(Student.Id.ToString()));
            DiPSClient.Publish("StudentReturned" + Student.Id.ToString(), new { Student = model });
        }

        public void Save(dynamic data)
        {
            try
            {
                StudentViewModel model = new StudentViewModel();
                model = data.ToObject<StudentViewModel>();
                model.Student.Id = model.Student.Id == Guid.Empty ? Guid.NewGuid() : model.Student.Id;
                model.Save();
            }
            catch
            {
                Errors.Add("Cannot Save the record");
            }
        }

        public void Delete(dynamic Student)
        {
            try
            {
                sRepo.Delete(new { Id = Student.Id });
            }
            catch (Exception e)
            {
                Errors.Add("Cannot Delete the record");
            }

        }

        //public void GetStudents(dynamic id)
        //{
        //    UpdateStudents();
        //}

        //private void UpdateStudents()
        //{
        //    //return the list of Students
        //    DiPSClient.Publish("StudentsUpdated", new { Students = sRepo.GetAll(), Errors = Errors });
        //    Errors.Clear();
        //}

        public async Task GetStudents(dynamic id)
        {
            await UpdateStudents();
        }

        private async Task UpdateStudents()
        {
            //return the list of Students
            StudentRepository repo = new StudentRepository();
            var students = await repo.GetAllAsync();
            DiPSClient.PublishAsync("StudentsUpdated", new { Students = students, Errors = Errors });
            Errors.Clear();
        }
        

        public void AddCourse(dynamic course)
        {
            using (var icRepo = new EnrollmentRepository())
            {
                icRepo.Insert(new Enrollment { Id = Guid.NewGuid(), StudentID = course.StudentId, CourseID = course.CourseId });
            }
        }

        public void DeleteCourse(dynamic course)
        {
            using (var icRepo = new EnrollmentRepository())
            {
                icRepo.Delete(where: new { CourseId = course.Id });
            }
        }
    }
}
