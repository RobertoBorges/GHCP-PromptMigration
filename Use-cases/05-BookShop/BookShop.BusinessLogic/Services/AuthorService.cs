using System;
using System.Collections.Generic;
using System.Text;
using BookShop.Common.Models;
using BookShop.DataAccess.Repositories;

namespace BookShop.BusinessLogic.Services
{
    public class AuthorService
    {
        private readonly AuthorRepository _authorRepository;

        public AuthorService()
        {
            _authorRepository = new AuthorRepository();
        }

        public List<Author> GetAllAuthors()
        {
            try
            {
                return _authorRepository.GetAllAuthors();
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error retrieving authors: " + ex.Message, ex);
            }
        }
    }
}