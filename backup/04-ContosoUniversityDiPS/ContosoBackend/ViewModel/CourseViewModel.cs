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
    public class CourseViewModel : ViewModelAutoLoadAndSave
    {

        [SelectFrom("Departments","DepartmentID","Department","Id","Name")]
        public Course Course { get; set; }

        public IList<Department> Departments { get; set; }

    }
}