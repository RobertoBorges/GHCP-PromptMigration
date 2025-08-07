using ContosoUniversity.Common.Interfaces;
using Microsoft.Extensions.Logging;
using System.Threading.Tasks;

namespace ContosoUniversity.Common.Services
{
    public class SmsSender : ISmsSender
    {
        private readonly ILogger<SmsSender> _logger;

        public SmsSender(ILogger<SmsSender> logger)
        {
            _logger = logger;
        }

        public Task SendSmsAsync(string phoneNumber, string message)
        {
            // In a real application, this would connect to an SMS service
            _logger.LogInformation("Phone Number: {PhoneNumber}, Message: {Message}", phoneNumber, message);
            return Task.CompletedTask;
        }
    }
}
