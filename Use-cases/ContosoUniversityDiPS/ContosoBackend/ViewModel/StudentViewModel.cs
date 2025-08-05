using ConUniv.Models;
using DataAccess.Scaffold.Attributes;
using DataAccess.Scaffold.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace ConUniv.ViewModels
{
    [NeedletailViewModel]
    public class StudentViewModel : ViewModelAutoLoadAndSave
    {

        [HasManyNtoN("Courses", "Id", "Enrollment", "StudentId", "CourseID", "Course", "Id")]
        public Student Student { get; set; }

        public IList<Course> Courses { get; set; }


        public override void FillData(string connectionString, object primaryKey, object me)
        {
            base.FillData(connectionString, primaryKey, me);
            if (this.Student.Id == Guid.Empty)
                this.Student.EnrollmentDate = DateTime.Now;
        }
    }
}