using System;


namespace FitnHealthy.Exceptions
{
    [Serializable]
    public class emptyStringException : Exception
    {
        public emptyStringException() : base("EXCEPTION: String cannot be empty!") { }

        public emptyStringException(string message) : base(message) { }
    }

    [Serializable]
    public class emailNotAvailableException : Exception
    {
        public emailNotAvailableException() : base("EXCEPTION: Email is not available!") { }

        public emailNotAvailableException(string message) : base(message) { }
    }

    [Serializable]
    public class emailNotValidException : Exception
    {
        public emailNotValidException() : base("EXCEPTION: The email is not a valid one!") { }

        public emailNotValidException(string message) : base(message) { }
    }

    [Serializable]
    public class userNotFoundException : Exception
    {
        public userNotFoundException() : base("EXCEPTION: User not found!") { }

        public userNotFoundException(string message) : base(message) { }
    }

    [Serializable]
    public class passwordsDontMatchException : Exception
    {
        public passwordsDontMatchException() : base("EXCEPTION: Passwords don't match!") { }

        public passwordsDontMatchException(string message) : base(message) { }
    }

    [Serializable]
    public class couldntFindHashException : Exception
    {
        public couldntFindHashException() : base("EXCEPTION: Couldn't find hash table in database!") { }

        public couldntFindHashException(string message) : base(message) { }
    }
}
