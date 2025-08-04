using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace ASPStoreModernized.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Products",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    Price = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    Description = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    ImageUrl = table.Column<string>(type: "nvarchar(255)", maxLength: 255, nullable: false),
                    Category = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false),
                    InStock = table.Column<bool>(type: "bit", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Products", x => x.Id);
                });

            migrationBuilder.InsertData(
                table: "Products",
                columns: new[] { "Id", "Category", "Description", "ImageUrl", "InStock", "Name", "Price" },
                values: new object[,]
                {
                    { 1, "", "A stylish desk lamp for your home office. Features adjustable brightness and color temperature settings. The lamp includes a USB charging port and touch controls.", "", true, "Classic Desk Lamp", 49.99m },
                    { 2, "", "Comfortable chair with lumbar support. Fully adjustable height, armrests, and recline settings. Breathable mesh back keeps you cool during long work sessions.", "", true, "Ergonomic Office Chair", 199.99m },
                    { 3, "", "Compact keyboard with quiet keys. Connects via Bluetooth to up to 3 devices simultaneously. Includes backlit keys and a rechargeable battery that lasts up to 2 weeks.", "", true, "Wireless Keyboard", 79.99m },
                    { 4, "", "24-inch full HD display. Features ultra-thin bezels, 144Hz refresh rate, and AMD FreeSync technology. Includes HDMI, DisplayPort, and USB-C connections.", "", true, "LED Monitor", 249.99m },
                    { 5, "", "Portable speaker with rich bass. Waterproof design makes it perfect for outdoor use. Provides up to 12 hours of playback on a single charge and includes a built-in microphone for calls.", "", true, "Bluetooth Speaker", 89.99m }
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Products");
        }
    }
}
