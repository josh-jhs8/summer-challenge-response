using Challenger.Model.Map;
using Challenger.Model.Player;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Contestant.Logic
{
    public class ExplorationManager
    {
        private List<Ship> _ships;
        private List<SolarSystem> _systems;
        private ShipManager _manager;
        

        public ExplorationManager(List<Ship> ships, List<SolarSystem> systems, ConnectionManager connection)
        {
            _ships = ships;
            _systems = systems;
            _manager = new ShipManager(connection);
        }

        public Task Explore()
        {
            return Task.Run(() =>
            {
                var accessableSystems = new List<string>();
                var shipPath = new Dictionary<Ship, Stack<string>>();

                while (true)
                {
                    foreach (var ship in _ships)
                    {
                        //First check we've recorded all the systems we're currently in
                        if (!_systems.Any(ss => ss.Name == ship.Location))
                        {
                            var newSystem = _manager.Observe(ship);
                            if (newSystem == null) continue;
                            _systems.Add(newSystem);
                            if (!accessableSystems.Contains(ship.Location)) accessableSystems.Add(ship.Location);
                            accessableSystems.AddRange(newSystem.Hyperlanes.Where(h => !accessableSystems.Contains(h)));
                        }
                    }

                    //This means we're done
                    if (accessableSystems.Count == _systems.Count) return;

                    foreach (var ship in _ships)
                    {
                        var currentSystem = _systems.First(ss => ss.Name == ship.Location);
                        var destination = currentSystem.Hyperlanes.FirstOrDefault(h => !_systems.Any(ss => ss.Name == h));
                        //If you've looked everywhere you can go from here, then go back
                        if (destination == null)
                        {
                            if (!shipPath.ContainsKey(ship)) continue;
                            destination = shipPath[ship].Pop();
                            if (shipPath[ship].Count == 0) shipPath.Remove(ship);
                        }
                        //Otherwise record the current location as part of the path
                        else
                        {
                            if (!shipPath.ContainsKey(ship)) shipPath.Add(ship, new Stack<string>());
                            shipPath[ship].Push(destination);
                        }

                        _manager.Move(ship, destination);
                    }
                }
            });
        }
    }
}
