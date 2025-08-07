namespace ContosoUniversity.Data
{
    public class AdminIdentityOptions
    {
        public string Role { get; } = "Administrator";
        public required string UserName { get; set; }
        public required string Password { get; set; }
    }
}
