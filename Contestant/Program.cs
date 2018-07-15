using Contestant.Logic;
using System;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;

namespace Contestant
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Press Enter to kill program");
            var task = LaunchNewChallenge();
            Console.ReadLine();
        }

        static Task LaunchNewChallenge()
        {
            return Task.Run(() =>
            {
                var host = Dns.GetHostEntry("localhost");
                var ipAddress = host.AddressList[host.AddressList.Length - 1];
                var remoteEndpoint = new IPEndPoint(ipAddress, 2092);

                using (var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp))
                {
                    socket.Connect(remoteEndpoint);
                    new ContestantManager(socket).PlayGame();
                }
            });
        }

        
    }
}
