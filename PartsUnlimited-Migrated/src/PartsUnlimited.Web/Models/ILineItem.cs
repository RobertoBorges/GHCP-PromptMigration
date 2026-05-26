namespace PartsUnlimited.Models
{
    public interface ILineItem
    {
        int Count { get; }
        Product Product { get; }
    }
}
