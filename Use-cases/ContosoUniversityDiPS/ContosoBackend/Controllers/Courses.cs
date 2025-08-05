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
    public class Courses : DiPSController
    {
        CourseRepository courseRepository;
        
        public Courses(DiPSClient client) : base(client) 
        {
            courseRepository = new CourseRepository();
        }


        public void GetCourse(dynamic course)
        {
            CourseViewModel model = new CourseViewModel();
            model.FillData(Guid.Parse(course.Id.ToString()));
            DiPSClient.Publish("CourseReturned" + course.Id.ToString(), new { course = model });
        }

        public void Save(dynamic data)
        {
            CourseViewModel model = new CourseViewModel();
            model = data.ToObject<CourseViewModel>();
            model.Course.Id = model.Course.Id == Guid.Empty ? Guid.NewGuid() : model.Course.Id;
            model.Save();
        }

        public void Delete(dynamic course)
        {
            courseRepository.Delete(new { Id = course.Id});
        }

        public void GetCourses(dynamic id)
        {
            UpdateCourses();
        }

        private void UpdateCourses()
        {
            //return the list of Courses
            DiPSClient.Publish("CoursesUpdated", new { courses = courseRepository.GetAll() });
        }


        public void SearchCourse(dynamic search)
        {
            var found = courseRepository.GetMany(where: new { Title_Like = search.query });
            var toReturn = found.Select(f => new { Name = f.Title, Id = f.Id }).OrderBy(i => i.Id);
            DiPSClient.Publish("CourseSearch" + search.id, toReturn);
        }

    }
}
