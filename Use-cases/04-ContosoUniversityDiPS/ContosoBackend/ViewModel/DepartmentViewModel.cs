using ConUniv.Models;
using ConUniv.Repositories;
using DataAccess.Scaffold.Attributes;
using DataAccess.Scaffold.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace ConUniv.ViewModels
{
    [NeedletailViewModel]
    public class DepartmentViewModel : ViewModelAutoLoadAndSave
    {
        

        public string InstructorIDName  { get; set; }

        public string StartDate { get; set; }

        [Autocomplete("InstructorID","Person","Id","FirstName","FirstName","FirstName")]
        public Department Department { get; set; }


        public override void FillData(string connectionString, object primaryKey, object me)
        {
            base.FillData(connectionString, primaryKey, me);
            if (this.Department.Id == Guid.Empty)
                this.Department.StartDate = DateTime.Now;
            FillOtherData();
        }

        public void FillOtherData() 
        {
            if (this.Department.InstructorID.HasValue)
            {
                using (var iRepo = new InstructorRepository())
                {
                    var inst = iRepo.GetSingle(where: new { Id = this.Department.InstructorID });
                    if (inst != null)                        
                        InstructorIDName = inst.FirstName + " " + inst.LastName;
                }
            }
            
            this.StartDate = this.Department.StartDate.ToShortDateString();
        }

    }
}