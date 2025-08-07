using System.Threading.Tasks;

namespace ContosoUniversity.Common.Interfaces
{
    public interface IEmailSender
    {
        Task SendEmailAsync(string email, string subject, string message);
    }
}
