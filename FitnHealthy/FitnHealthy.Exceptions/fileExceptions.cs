using System;

namespace FitnHealthy.Exceptions
{
    [Serializable]
    public class FileDoesntExistException : Exception
    {
        public FileDoesntExistException() : base("EXCEPTION: File doesn't exist!") { }
        
        public FileDoesntExistException(string message) : base(message) { }

    }

    [Serializable]
    public class FileNotCompleteException : Exception
    {
        public FileNotCompleteException() : base("EXCEPTION: File doesn't have enough data!") { }

        public FileNotCompleteException(string message) : base(message) { }
    }
}
