using Challenger.Model.PlayerAction;
using Newtonsoft.Json;
using System;
using System.Net.Sockets;
using System.Text;

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

        public CommandResult<TReturnType> SendCommand<TReturnType>(Command command)
        {
            var cmdJson = JsonConvert.SerializeObject(command);
            Console.WriteLine($"Sending: {cmdJson}");
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
            Console.WriteLine($"Received: {resultJson}");
            return JsonConvert.DeserializeObject<CommandResult<TReturnType>>(resultJson);
        }

        public void Close()
        {
            _connection.Close();
        }
    }
}
