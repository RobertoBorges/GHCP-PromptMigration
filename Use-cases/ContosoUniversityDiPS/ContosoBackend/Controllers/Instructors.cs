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
    public class Instructors : DiPSController
    {

        InstructorRepository iRepo;
        List<string> Errors;

        public Instructors(DiPSClient client) : base(client) 
        {
            iRepo = new InstructorRepository();
            Errors = new List<string>();
        }



        public void GetInstructor(dynamic Instructor)
        {
            InstructorViewModel model = new InstructorViewModel();
            model.FillData(Guid.Parse(Instructor.Id.ToString()));
            DiPSClient.Publish("InstructorReturned" + Instructor.Id.ToString(), new { Instructor = model });
        }

        public void Save(dynamic data)
        {
            try
            {
                InstructorViewModel model = new InstructorViewModel();
                model = data.ToObject<InstructorViewModel>();
                model.Instructor.Id = model.Instructor.Id == Guid.Empty ? Guid.NewGuid() : model.Instructor.Id;
                model.Save();
            }
            catch
            {
                Errors.Add("Cannot Save the record");
            }
        }

        public void Delete(dynamic Instructor)
        {
            try
            {
                iRepo.Delete(new { Id = Instructor.Id });
            }
            catch (Exception e)
            {
                Errors.Add("Cannot Delete the record");
            }

        }

        public void GetInstructors(dynamic id)
        {
            UpdateInstructors();
        }

        private void UpdateInstructors()
        {
            //return the list of Instructors
            DiPSClient.Publish("InstructorsUpdated", new { Instructors = iRepo.GetAll(), Errors = Errors });
            Errors.Clear();
        }
        public void SearchInstructor(dynamic search)
        {
            var found = iRepo.GetMany(where: new {  FirstName_Like = search.query, Or_LastName_Like = search.query });
            var toReturn = found.Select(f=> new { Name = f.FirstName + " " + f.LastName , Id = f.Id } ).OrderBy(i=> i.Id);
            DiPSClient.Publish("InstructorSearch" + search.id, toReturn);
        }

        public void AddCourse(dynamic course)
        {
            using (var icRepo = new CourseInstructorRepository())
            {
                icRepo.Insert(new CourseInstructor { Id = Guid.NewGuid(), InstructorID = course.InstructorId, CourseID = course.CourseId });
            }
        }

        public void DeleteCourse(dynamic course)
        {
            using (var icRepo = new CourseInstructorRepository())
            {
                icRepo.Delete(where: new { CourseId = course.Id });
            }
        }

    }
}
