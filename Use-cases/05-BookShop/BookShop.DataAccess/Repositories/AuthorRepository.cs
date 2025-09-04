using System;
using System.Collections.Generic;
using System.Text;
using System.Data;
using BookShop.Common.Models;
using BookShop.DataAccess.Base;

namespace BookShop.DataAccess.Repositories
{
    public class AuthorRepository : BaseRepository
    {
        public List<Author> GetAllAuthors()
        {
            string query = "SELECT * FROM Authors WHERE IsActive = 1 ORDER BY LastName, FirstName";
            DataTable dataTable = ExecuteQuery(query);
            return ConvertDataTableToAuthors(dataTable);
        }

        private List<Author> ConvertDataTableToAuthors(DataTable dataTable)
        {
            List<Author> authors = new List<Author>();
            foreach (DataRow row in dataTable.Rows)
            {
                authors.Add(new Author
                {
                    AuthorId = Convert.ToInt32(row["AuthorId"]),
                    FirstName = row["FirstName"].ToString(),
                    LastName = row["LastName"].ToString(),
                    Biography = row["Biography"].ToString(),
                    BirthDate = row["BirthDate"] != DBNull.Value ? (DateTime?)Convert.ToDateTime(row["BirthDate"]) : null,
                    Nationality = row["Nationality"].ToString(),
                    PhotoUrl = row["PhotoUrl"].ToString(),
                    IsActive = Convert.ToBoolean(row["IsActive"]),
                    CreatedDate = Convert.ToDateTime(row["CreatedDate"]),
                    ModifiedDate = Convert.ToDateTime(row["ModifiedDate"])
                });
            }
            return authors;
        }
    }
}