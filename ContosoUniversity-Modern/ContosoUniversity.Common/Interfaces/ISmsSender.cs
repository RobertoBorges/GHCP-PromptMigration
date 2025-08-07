using System.Threading.Tasks;

namespace ContosoUniversity.Common.Interfaces
{
    public interface ISmsSender
    {
        Task SendSmsAsync(string phoneNumber, string message);
    }
}
