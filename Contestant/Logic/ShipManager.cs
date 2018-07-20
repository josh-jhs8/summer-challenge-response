using ChallengeModel.Map;
using ChallengeModel.Player;
using ChallengeModel.PlayerAction;
using System.Collections.Generic;

namespace Contestant.Logic
{
    public class ShipManager
    {
        private ConnectionManager _connection;

        public ShipManager(ConnectionManager connection)
        {
            _connection = connection;
        }

        public SolarSystem Observe(Ship ship)
        {
            var command = new Command()
            {
                Type = "Ship",
                Subject = ship.Name,
                Action = "Observe",
                Arguments = new List<string>()
            };
            var result = _connection.SendCommand<SolarSystem>(command);
            if (result.Success) return result.ResultObject;
            else return null;
        }

        public void Move(Ship ship, string destination)
        {
            var command = new Command()
            {
                Type = "Ship",
                Subject = ship.Name,
                Action = "Move",
                Arguments = new List<string>() { destination }
            };
            var result = _connection.SendCommand<Ship>(command);
            if (result.Success) ship.Location = result.ResultObject.Location;
        }
    }
}
