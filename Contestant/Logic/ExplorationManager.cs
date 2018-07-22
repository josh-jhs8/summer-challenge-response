using Contestant.Model;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace Contestant.Logic
{
    public class ExplorationManager
    {
        private ChallengeState _state;
        private ShipManager _manager;
        

        public ExplorationManager(ChallengeState state, ConnectionManager connection)
        {
            _state = state;
            _manager = new ShipManager(connection);
        }

        public Task Explore()
        {
            return Task.Run(() =>
            {
                var accessableSystems = new List<string>();
                var shipPath = new Dictionary<string, Stack<string>>();

                while (true)
                {
                    if (_state.Ships.Count < 1)
                    {
                        Thread.Sleep(100);
                        continue;
                    }

                    foreach (var ship in _state.Ships.Select(s => s.Value).Where(s => s.Status == "Awaiting Command"))
                    {
                        //First check we've recorded all the systems we're currently in
                        if (!_state.SolarSystems.ContainsKey(ship.Location))
                        {
                            var newSystem = _manager.Observe(ship);
                            if (newSystem == null) continue;
                            _state.SolarSystems.AddOrUpdate(newSystem.Name, newSystem, (n, s) => newSystem);
                            if (!accessableSystems.Contains(ship.Location)) accessableSystems.Add(ship.Location);
                            accessableSystems.AddRange(newSystem.Hyperlanes.Where(h => !accessableSystems.Contains(h)));
                        }
                    }

                    //This means we're done
                    if (accessableSystems.Count == _state.SolarSystems.Count) return;

                    foreach (var ship in _state.Ships.Select(s => s.Value).Where(s => s.Status == "Awaiting Command"))
                    {
                        if (!_state.SolarSystems.ContainsKey(ship.Location)) continue;
                        var currentSystem = _state.SolarSystems[ship.Location];
                        var destination = currentSystem.Hyperlanes.FirstOrDefault(h => !_state.SolarSystems.ContainsKey(h));
                        //If you've looked everywhere you can go from here, then go back
                        if (destination == null)
                        {
                            if (!shipPath.ContainsKey(ship.Name)) continue;
                            destination = shipPath[ship.Name].Pop();
                            if (shipPath[ship.Name].Count == 0) shipPath.Remove(ship.Name);
                        }
                        //Otherwise record the current location as part of the path
                        else
                        {
                            if (!shipPath.ContainsKey(ship.Name)) shipPath.Add(ship.Name, new Stack<string>());
                            shipPath[ship.Name].Push(currentSystem.Name);
                        }

                        _manager.Move(ship, destination);
                        _state.Ships.AddOrUpdate(ship.Name, ship, (n, s) => ship);
                    }
                }
            });
        }
    }
}
