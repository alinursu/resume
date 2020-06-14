using System.ComponentModel.DataAnnotations;

namespace FitnHealthy.Models
{
    public class AccountCredentials
    {
        /*
            Model pentru credentialele unui cont (email si parola).
        */

        [Required(ErrorMessage = "Acest camp este necesar!")]
        public string email { get; set; }

        [Required(ErrorMessage = "Acest camp este necesar!")]
        [DataType(DataType.Password)]
        public string password { get; set; }
    }
}
