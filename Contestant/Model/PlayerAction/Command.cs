using System.Collections.Generic;

namespace Challenger.Model.PlayerAction
{
    public class Command
    {
        public string Type { get; set; }

        public string Subject { get; set; }

        public string Action { get; set; }

        public List<string> Arguments { get; set; }

        public string ExpectedReturnType { get; set; }
    }
}
