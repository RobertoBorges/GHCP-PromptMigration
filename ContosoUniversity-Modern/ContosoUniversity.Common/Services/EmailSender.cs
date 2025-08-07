using ContosoUniversity.Common.Interfaces;
using Microsoft.Extensions.Logging;
using System.Threading.Tasks;

namespace ContosoUniversity.Common.Services
{
    public class EmailSender : IEmailSender
    {
        private readonly ILogger<EmailSender> _logger;

        public EmailSender(ILogger<EmailSender> logger)
        {
            _logger = logger;
        }

        public Task SendEmailAsync(string email, string subject, string message)
        {
            // In a real application, this would connect to an email service
            _logger.LogInformation("Email: {Email}, Subject: {Subject}, Message: {Message}", email, subject, message);
            return Task.CompletedTask;
        }
    }
}
