using Contestant.Model;
using System;
using System.Linq;
using System.Net.Sockets;

namespace Contestant.Logic
{
    public class ContestantManager
    {
        private ConnectionManager _connection;

        public ContestantManager(Socket connection)
        {
            _connection = new ConnectionManager(connection);
        }

        public void PlayGame()
        {
            var state = new ChallengeState();
            var stateManager = new StateManager(_connection, state);
            stateManager.PollState();

            new ExplorationManager(state, _connection).Explore().Wait();
            stateManager.Finish();

            foreach (var system in state.SolarSystems.Select(s => s.Value))
            {
                Console.WriteLine(system.Name);
            }

            _connection.Close();
        }
    }
}
