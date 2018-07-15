using Challenger.Model.Map;
using Challenger.Model.Player;
using Challenger.Model.PlayerAction;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace Contestant.Logic
{
    public class ContestantManager
    {
        private ConnectionManager _connection;
        private List<Ship> _ships = new List<Ship>();
        private List<SolarSystem> _systems = new List<SolarSystem>();

        public ContestantManager(Socket connection)
        {
            _connection = new ConnectionManager(connection);
        }

        public void PlayGame()
        {
            GetListOfShips();

            new ExplorationManager(_ships, _systems, _connection).Explore().Wait();

            foreach (var system in _systems)
            {
                Console.WriteLine(system.Name);
            }

            _connection.Close();
        }

        private void GetListOfShips()
        {
            var command = new Command
            {
                Type = "Ship",
                Subject = "",
                Action = "List",
                Arguments = new List<string>()
            };
            var result = _connection.SendCommand<List<Ship>>(command);
            if (result.Success)
            {
                _ships = result.ResultObject;
                Console.WriteLine("Got list of ships:");
                foreach (var ship in _ships) Console.WriteLine($"\t{ship.Name}");
            }
            else
            {
                Console.WriteLine($"Failed to get ships: {result.Message}");
            }
        }
    }
}
