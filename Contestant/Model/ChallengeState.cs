using ChallengeModel.Map;
using System.Collections.Concurrent;

namespace Contestant.Model
{
    public class ChallengeState
    {
        public ConcurrentDictionary<string, SolarSystem> SolarSystems { get; set; } = new ConcurrentDictionary<string, SolarSystem>();

        public ChallengeEmpire Empire { get; set; } = new ChallengeEmpire();
    }
}
