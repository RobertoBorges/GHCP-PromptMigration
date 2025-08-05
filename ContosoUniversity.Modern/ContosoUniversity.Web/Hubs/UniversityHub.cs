using Microsoft.AspNetCore.SignalR;
using System;
using System.Threading.Tasks;

namespace ContosoUniversity.Web.Hubs
{
    public class UniversityHub : Hub
    {
        // Student notifications
        public async Task NotifyStudentAdded(string firstName, string lastName)
        {
            await Clients.All.SendAsync("StudentAdded", firstName, lastName);
        }
        
        public async Task NotifyStudentUpdated(string id, string firstName, string lastName)
        {
            await Clients.All.SendAsync("StudentUpdated", id, firstName, lastName);
        }
        
        public async Task NotifyStudentDeleted(string id)
        {
            await Clients.All.SendAsync("StudentDeleted", id);
        }
        
        // Course notifications
        public async Task NotifyCourseAdded(string title, int credits)
        {
            await Clients.All.SendAsync("CourseAdded", title, credits);
        }
        
        public async Task NotifyCourseUpdated(string id, string title)
        {
            await Clients.All.SendAsync("CourseUpdated", id, title);
        }
        
        public async Task NotifyCourseDeleted(string id)
        {
            await Clients.All.SendAsync("CourseDeleted", id);
        }
        
        // Instructor notifications
        public async Task NotifyInstructorAdded(string firstName, string lastName)
        {
            await Clients.All.SendAsync("InstructorAdded", firstName, lastName);
        }
        
        public async Task NotifyInstructorUpdated(string id, string firstName, string lastName)
        {
            await Clients.All.SendAsync("InstructorUpdated", id, firstName, lastName);
        }
        
        public async Task NotifyInstructorDeleted(string id)
        {
            await Clients.All.SendAsync("InstructorDeleted", id);
        }
        
        // Department notifications
        public async Task NotifyDepartmentAdded(string name)
        {
            await Clients.All.SendAsync("DepartmentAdded", name);
        }
        
        public async Task NotifyDepartmentUpdated(string id, string name)
        {
            await Clients.All.SendAsync("DepartmentUpdated", id, name);
        }
        
        public async Task NotifyDepartmentDeleted(string id)
        {
            await Clients.All.SendAsync("DepartmentDeleted", id);
        }
    }
}
