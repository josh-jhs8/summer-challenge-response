using ChallengeModel.Player;
using System.Collections.Concurrent;
using System.Collections.Generic;

namespace Contestant.Model
{
    public class ChallengeEmpire
    {
        public string Name { get; set; } = string.Empty;
        public ConcurrentDictionary<string, Ship> Ships { get; set; } = new ConcurrentDictionary<string, Ship>();

        public void UpdateShips(List<Ship> ships)
        {
            foreach (var ship in ships) Ships.AddOrUpdate(ship.Name, ship, (n, s) => ship);
        }
    }
}
