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
    public class InstructorViewModel : ViewModelAutoLoadAndSave
    {

        [HasOne("Office", "Id", "OfficeAssignment", "InstructorID")]
        [HasManyNtoN("Courses","Id","CourseInstructor","InstructorId","CourseID","Course","Id")]
        public Instructor Instructor { get; set; }

        public OfficeAssignment Office { get; set; }

        public IList<Course> Courses { get; set; }


        public override void FillData(string connectionString, object primaryKey, object me)
        {
            base.FillData(connectionString, primaryKey, me);
            if (this.Instructor.Id == Guid.Empty)
                this.Instructor.HireDate = DateTime.Now;
        }
    }
}