using System;
using System.Collections.Generic;

namespace FitnHealthy.DatabaseCommunication
{
    class Hash
    {
        private string hash;
        private string symbols = "!@#$%^&*?><|~`1234567890/.,";
        private string characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !@#$%^&*()-_=+[{]};:'\"\\|,./?`~";
        private List<string> hashVector;

        public Hash(string hash)
        {
            this.hash = hash;
            this.buildHashVector();
        }

        private void buildHashVector()
        {
            /*
             * Construieste un vector cu codurile caracterelor, folosindu-se de hash.
            */
            string code;
            hashVector = new List<string>();

            for (int i = 0; i < hash.Length; i += 4)
            {
                code = "";
                code = code.Insert(code.Length, Convert.ToString(hash[i]));
                code = code.Insert(code.Length, Convert.ToString(hash[i + 1]));
                code = code.Insert(code.Length, Convert.ToString(hash[i + 2]));
                code = code.Insert(code.Length, Convert.ToString(hash[i + 3]));
                hashVector.Insert(hashVector.Count, code);
            }

            hashVector.RemoveAt(0);
            hashVector.RemoveAt(0);
            hashVector.RemoveAt(0);
            hashVector.RemoveAt(0);
            hashVector.RemoveAt(hashVector.Count - 1);
            hashVector.RemoveAt(hashVector.Count - 1);
            hashVector.RemoveAt(hashVector.Count - 1);
        }

        private string encryptPrivate(string text)
        {
            /*
             * Cripteaza un text folosindu-se de hash.
            */
            string output = "";

            // Creez output-ul
            for (int i = 0; i < text.Length; i++)
                output = output.Insert(output.Length, hashVector[characters.IndexOf(text[i])]);

            return output;
        }

        private string decryptPrivate(string text)
        {
            /*
             * Descifreaza un text folosindu-se de hash.
            */
            string output = "";
            string code;

            // Decodific text
            for (int i = 0; i < text.Length; i += 4)
            {
                code = "";
                code = code.Insert(code.Length, Convert.ToString(text[i]));
                code = code.Insert(code.Length, Convert.ToString(text[i + 1]));
                code = code.Insert(code.Length, Convert.ToString(text[i + 2]));
                code = code.Insert(code.Length, Convert.ToString(text[i + 3]));

                // Caut code in hash list si adaug caracterul respectiv in output
                output = output.Insert(output.Length, Convert.ToString(characters[hashVector.IndexOf(code)]));
            }

            return output;
        }

        public string Encrypt(string text)
        {
            /*
                Cripteaza un text.
            */
            return this.encryptPrivate(text);
        }

        public string Decrypt(string text)
        {
            /*
                Decripteaza un text.
            */
            return this.decryptPrivate(text);
        }

        ~Hash()
        {
            hash = "";
            symbols = "";
            characters = "";
            hashVector = null;
        }
    }
}
