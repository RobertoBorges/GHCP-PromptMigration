using System;
using System.Collections.Generic;
using System.Text;
using System.Data;
using BookShop.Common.Models;
using BookShop.DataAccess.Base;

namespace BookShop.DataAccess.Repositories
{
    public class CategoryRepository : BaseRepository
    {
        public List<Category> GetAllCategories()
        {
            string query = "SELECT * FROM Categories WHERE IsActive = 1 ORDER BY Name";
            DataTable dataTable = ExecuteQuery(query);
            return ConvertDataTableToCategories(dataTable);
        }

        private List<Category> ConvertDataTableToCategories(DataTable dataTable)
        {
            List<Category> categories = new List<Category>();
            foreach (DataRow row in dataTable.Rows)
            {
                categories.Add(new Category
                {
                    CategoryId = Convert.ToInt32(row["CategoryId"]),
                    Name = row["Name"].ToString(),
                    Description = row["Description"].ToString(),
                    IsActive = Convert.ToBoolean(row["IsActive"]),
                    CreatedDate = Convert.ToDateTime(row["CreatedDate"]),
                    ModifiedDate = Convert.ToDateTime(row["ModifiedDate"])
                });
            }
            return categories;
        }
    }
}