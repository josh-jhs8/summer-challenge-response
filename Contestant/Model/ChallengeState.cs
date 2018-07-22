using ChallengeModel.Map;
using ChallengeModel.Player;
using System.Collections.Concurrent;

namespace Contestant.Model
{
    public class ChallengeState
    {
        public ConcurrentDictionary<string, SolarSystem> SolarSystems { get; set; } = new ConcurrentDictionary<string, SolarSystem>();

        public ConcurrentDictionary<string, Ship> Ships { get; set; } = new ConcurrentDictionary<string, Ship>();
    }
}
