using System.ComponentModel.DataAnnotations;

namespace FitnHealthy.Models
{
    public class Account
    {
        /*
            Model pentru cont. 
            Retine toate informatiile legate de un cont.
        */
        [Required(ErrorMessage = "Acest camp este necesar!")]
        public string lastName { get; set; }

        [Required(ErrorMessage = "Acest camp este necesar!")]
        public string firstName { get; set; }

        [Required(ErrorMessage = "Acest camp este necesar!")]
        public string email { get; set; }

        [Required(ErrorMessage = "Acest camp este necesar!")]
        [DataType(DataType.Password)]
        public string password { get; set; }

        [Required(ErrorMessage = "Acest camp este necesar!")]
        public string experience { get; set; }
    }
}
