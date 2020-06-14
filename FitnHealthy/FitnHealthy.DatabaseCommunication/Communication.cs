using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.IO;
using FitnHealthy.Exceptions;

namespace FitnHealthy.DatabaseCommunication
{
    public class dbCommunication
    {
        /*
            Creeaza o conexiune cu baza de date prin care preia date sau scrie date in ea. 
        */
        private string connectionString;
        private SqlConnection connection;
        private Hash hash;

        static private string stringNoBlankSpaces(string str)
        {
            /*
             * Sterge caracterele spatiu de la final si returneaza noul string.
            */
            int temp = 0;
            for (int i = str.Length - 1; i >= 0; i--)
            {
                if (str[i] != ' ')
                {
                    temp = i;
                    break;
                }
            }

            return str.Substring(0, temp + 1);
        }

        private void buildConnectionString()
        {
            /* Construieste un connection string din datele citite din fisierul config.cfg. */

            // Preiau directorul in care se afla fisierul config.cfg
            string configDirectory = Directory.GetCurrentDirectory() + "\\" + "wwwroot" + "\\";

            // Verific daca fisierul config.cfg exista
            if (File.Exists(configDirectory + "config.cfg") == false)
                throw new FileDoesntExistException("ERROR! Fisierul config.cfg nu exista!");

            // Citesc fisierul config.cfg
            string fileContent;
            using (StreamReader strdr = new StreamReader(configDirectory + "config.cfg"))
            {
                fileContent = strdr.ReadToEnd();
            }
            string serverName = fileContent.Split("\n")[0].Split("=")[1].ToString();
            serverName = serverName.Remove(serverName.Length-1, 1);
            if (serverName.Length == 0)
                throw new FileNotCompleteException("ERROR! Fisierul config.cfg nu contine numele serverului!");
            string databaseName = fileContent.Split("\n")[1].Split("=")[1].ToString();
            if (databaseName.Length == 0)
                throw new FileNotCompleteException("ERROR! Fisierul config.cfg nu contine numele bazei de date!");

            // Creez connection string-ul
            this.connectionString = "Server=" + serverName + ";Database=" + databaseName + ";Trusted_Connection=true;MultipleActiveResultSets=true";
        }

        private string readHash()
        {
            /*
                Citesc hash-ul din baza de date.
            */
            string sqlString = "SELECT * FROM hash";
            SqlCommand sqlCmd = new SqlCommand(sqlString, connection);
            SqlDataReader dataReader = sqlCmd.ExecuteReader();
            string hash;
            if (dataReader.Read())
                hash = stringNoBlankSpaces(dataReader["text"].ToString());
            else
                throw new couldntFindHashException();
            sqlCmd.Dispose();
            return hash;
        }

        private int numberOfRowsFromTable(string tableName)
        {
            /*
                Returneaza numarul de linii din tabela "tableName".
            */
            string sqlString = $"SELECT * FROM {tableName.ToString()}";
            SqlCommand sqlCmd = new SqlCommand(sqlString, connection);
            SqlDataReader dataReader = sqlCmd.ExecuteReader();
            int count = 0;

            while (dataReader.Read())
                count++;

            return count;
        }

        private List<KeyValuePair<int, List<string>>> getUsersTableContent(string condition=null)
        {
            /*
                Returneaza o lista cu toate liniile din tabela "users".
                Optional, se poate seta o clauza (WHERE), astfel incat se vor lua din tabela doar liniile dorite.
            */
            string tableName = "users";
            List<KeyValuePair<int, List<string>>> list = new List<KeyValuePair<int, List<string>>>(numberOfRowsFromTable(tableName));
            string sqlString;
            if (condition == null)
                sqlString = $"SELECT * FROM {tableName.ToString()}";
            else
                sqlString = $"SELECT * FROM {tableName.ToString()} WHERE {condition.ToString()}";
            SqlCommand sqlCmd = new SqlCommand(sqlString, connection);
            SqlDataReader dataReader = sqlCmd.ExecuteReader();
            List<string> tempList;

            while(dataReader.Read())
            {
                tempList = new List<string>(5);
                tempList.Add(dataReader["lastName"].ToString());
                tempList.Add(dataReader["firstName"].ToString());
                tempList.Add(dataReader["email"].ToString());
                tempList.Add(dataReader["password"].ToString());
                tempList.Add(dataReader["experience"].ToString());
                list.Add(new KeyValuePair<int, List<string>>(Convert.ToInt32(dataReader["id"].ToString()), tempList));
            }

            return list;
        }



        public void updateTable(string tableName, string newValues, string identificator)
        {
            /*
                Scrie in tabela "tableName" noile valori, stocate in "newValues", pe linia gasita cu "identificator" (de obicei, ID).
            */
            // Criptez datele din "newValues"
            string temp = newValues.Substring(0, newValues.IndexOf("'")) + "'";
            newValues = newValues.Substring(newValues.IndexOf("'") + 1, newValues.Length - newValues.IndexOf("'")-1);
            temp = temp + hash.Encrypt(newValues.Substring(0, newValues.IndexOf("'"))) + "'";
            newValues = newValues.Substring(newValues.IndexOf("'") + 1, newValues.Length - newValues.IndexOf("'") - 1);

            while((newValues.Length != 0) && (newValues.IndexOf("'") != -1))
            {
                temp = temp + newValues.Substring(0, newValues.IndexOf("'")) + "'";
                newValues = newValues.Substring(newValues.IndexOf("'") + 1, newValues.Length - newValues.IndexOf("'")-1);
                temp = temp + hash.Encrypt(newValues.Substring(0, newValues.IndexOf("'"))) + "'";
                newValues = newValues.Substring(newValues.IndexOf("'") + 1, newValues.Length - newValues.IndexOf("'") - 1);
            }

            newValues = temp;

            // Aplic update-ul asupra tabelei "tableName"
            string sqlString = $"UPDATE {tableName} SET {newValues} WHERE {identificator}";
            SqlCommand sqlCmd = new SqlCommand(sqlString, connection);
            sqlCmd.ExecuteNonQuery();
            sqlCmd.Dispose();
        }

        private bool verifyEmailIsAvailable(string email)
        {
            /*
                Verifica daca email-ul este disponibil (daca exista deja un cont creat cu acest email sau nu).
            */
            return (getUsersTableContent($"email='{hash.Encrypt(email)}'").Count == 0);
        }

        public int addNewUser(string lastName, string firstName, string email, string password, string experience)
        {
            /*
                Adauga informatii in tabela "users" (creeaza un cont nou). 
                Returneaza id-ul contului daca a fost creat sau -1 daca a aparut o eroare.
            */
            if (verifyEmailIsAvailable(email) == false)
                throw new emailNotAvailableException("ERROR! The email is linked to an existing account!");
            try
            {
                string sqlString = $"INSERT INTO users(lastName, firstName, email, password, experience) VALUES ('{hash.Encrypt(lastName.ToString())}', '{hash.Encrypt(firstName.ToString())}', '{hash.Encrypt(email.ToString())}', '{hash.Encrypt(password.ToString())}', '{hash.Encrypt(experience.ToString())}')";
                SqlCommand sqlCmd = new SqlCommand(sqlString, connection);
                sqlCmd.ExecuteNonQuery();
                sqlCmd.Dispose();
                return this.getUsersTableContent($"email='{hash.Encrypt(email.ToString())}'")[0].Key;
            }
            catch(Exception e)
            {
                return -1;
            }
        }

        public int checkCredentialsUser(string email, string password)
        {
            /*
                Verifica daca contul exista in baza de date. Daca da, returneaza id-ul contului. Daca nu, returneaza -1.
            */
            List<KeyValuePair<int, List<string>>> temp = getUsersTableContent($"email='{hash.Encrypt(email)}' AND password='{hash.Encrypt(password)}'");
            if (temp.Count == 0)
                return -1;
            return temp[0].Key;
        }
        

        public void openConnection()
        {
            /*
                Creeaza conexiunea cu baza de date.
            */
            connection = new SqlConnection(connectionString);
            connection.Open();
        }

        public void closeConnection()
        {
            /*
                Inchide conexiunea cu baza de date.
            */
            connection.Close();
        }

        public dbCommunication()
        {
            buildConnectionString();
            openConnection();
            hash = new Hash(readHash());
            closeConnection();
        }

        ~dbCommunication()
        {
            this.connectionString = null;
            try
            {
                closeConnection();
            }
            catch(Exception e)
            {
                
            }
        }

        
    }
}
