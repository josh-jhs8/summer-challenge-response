using ChallengeModel;
using ChallengeModel.Map;
using ChallengeModel.Player;
using ChallengeModel.PlayerAction;
using Contestant.Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace Contestant.Logic
{
    public class StateManager
    {
        private ConnectionManager _connection;
        private ChallengeState _state;
        private bool _active = true;
        private object _activeLock = new object();

        public StateManager(ConnectionManager connection, ChallengeState state)
        {
            _connection = connection;
            _state = state;
        }

        public void PollState()
        {
            Task.Run(() =>
            {
                var running = true;
                while (running)
                {
                    var cmd = new Command
                    {
                        Type = "State",
                        Action = "Poll",
                        Subject = string.Empty,
                        Arguments = new List<string>()
                    };
                    var result = _connection.SendCommand<State>(cmd);
                    if (!result.Success) throw new Exception("Something went wrong with the poll state command.");
                    var newState = result.ResultObject;
                    UpdateEmpire(newState.Players.First());
                    UpdateSystems(newState.SolarSystems);
                    Thread.Sleep(100);
                    lock(_activeLock) { running = _active; }
                }
            });
        }

        public void Finish()
        {
            lock(_activeLock) { _active = false; }
        }

        private void UpdateEmpire(Empire empire)
        {
            if (string.IsNullOrEmpty(_state.Empire.Name)) _state.Empire.Name = empire.Name;
            if (_state.Empire.Name == empire.Name)
            {
                _state.Empire.UpdateShips(empire.Ships);
            }
        }

        private void UpdateSystems(List<SolarSystem> systems)
        {
            foreach (var system in systems)
            {
                _state.SolarSystems.AddOrUpdate(system.Name, system, (n, s) => system);
            }
        }
    }
}
