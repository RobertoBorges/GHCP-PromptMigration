using DiPSBackEndApplication.Application;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ContosoBackend
{
    class Program : DiPSBackEnd
    {
        static Program()
        {
            //Initialize the backend, this setup the connection with DiPS and registers all the controllers with the public methods
            InitializeBackEnd();

        }

        static void Main(string[] args)
        {
            //Migrations to recreate the database if needed
            Needletail.DataAccess.Migrations.Migrator.Migrate("Default");

            //wait for a key
            while (true)
            {
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("Contoso University backend");
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Type exit to finish this process");
                Console.ForegroundColor = ConsoleColor.Yellow;
                var e = Console.ReadLine();
                if (e.Trim().ToLower() == "exit")
                    break;
            }

        }
    }
}
