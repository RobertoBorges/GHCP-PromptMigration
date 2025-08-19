using System;
using System.Collections.Generic;
using System.Text;
using BookShop.Common.Models;
using BookShop.DataAccess.Repositories;

namespace BookShop.BusinessLogic.Services
{
    public class CategoryService
    {
        private readonly CategoryRepository _categoryRepository;

        public CategoryService()
        {
            _categoryRepository = new CategoryRepository();
        }

        public List<Category> GetAllCategories()
        {
            try
            {
                return _categoryRepository.GetAllCategories();
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error retrieving categories: " + ex.Message, ex);
            }
        }
    }
}