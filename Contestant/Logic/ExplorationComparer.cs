using System.Collections.Generic;
using System.Linq;

namespace Contestant.Logic
{
    public class ExplorationComparer : IComparer<string>
    {
        private IEnumerable<string> _visitedByShips;
        private IEnumerable<string> _plannedDestinations;

        public ExplorationComparer(Dictionary<string, List<string>> visitedByShips, Dictionary<string, string> plannedDestinations)
        {
            _visitedByShips = visitedByShips.Select(d => d.Value).SelectMany(x => x);
            _plannedDestinations = plannedDestinations.Select(d => d.Value);
        }

        public int Compare(string x, string y)
        {
            return Rate(y) - Rate(x);
        }

        private int Rate(string destination)
        {
            if (!_visitedByShips.Contains(destination))
            {
                if (!_plannedDestinations.Contains(destination)) return 3;
                return 2;
            }
            return 1;
        }
    }
}
