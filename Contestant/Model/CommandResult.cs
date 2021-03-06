﻿namespace Challenger.Model
{
    public class CommandResult<T>
    {
        public bool Success { get; set; }

        public string Message { get; set; }

        public T ResultObject { get; set; }
    }
}
