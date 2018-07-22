using ChallengeModel.PlayerAction;
using Challenger.Model;
using Newtonsoft.Json;
using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Contestant.Logic
{
    public class ConnectionManager
    {
        private Socket _connection;
        private object _processingLock = new object();

        public ConnectionManager(Socket connection)
        {
            _connection = connection;
        }

        public Task PollForStart()
        {
            return Task.Run(() =>
            {
                while (true)
                {
                    var data = new byte[10];
                    var dataSize = _connection.Receive(data);
                    if (dataSize > 0)
                    {
                        var resultData = new byte[dataSize];
                        Array.Copy(data, resultData, dataSize);
                        var result = Encoding.UTF8.GetString(resultData);
                        if (result == "Begin") return;
                    }
                    Thread.Sleep(100);
                }
            });
        }

        public CommandResult<TReturnType> SendCommand<TReturnType>(Command command)
        {
            var cmdJson = JsonConvert.SerializeObject(command);
            var cmd = Encoding.UTF8.GetBytes(cmdJson);

            byte[] data = new byte[1000000];
            int dataSize;
            lock (_processingLock)
            {
                _connection.Send(cmd);
                dataSize = _connection.Receive(data);
            }
            
            byte[] resultData = new byte[dataSize];
            Array.Copy(data, resultData, dataSize);

            var resultJson = Encoding.UTF8.GetString(resultData);
            return JsonConvert.DeserializeObject<CommandResult<TReturnType>>(resultJson);
        }

        public void Close()
        {
            _connection.Close();
        }
    }
}
