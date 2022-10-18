#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#define PORT 8080

using namespace std;

int main() {
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        fprintf(stderr, "Socket creation failed!\n");
        return 1;
    } // end if

    struct sockaddr_in recv_address;
    recv_address.sin_family = AF_INET;
    recv_address.sin_addr.s_addr = INADDR_ANY;
    recv_address.sin_port = htons(PORT);

    // Forcefully attaching socket to the port 8080
    if (bind(sockfd, (struct sockaddr*)&recv_address, sizeof(recv_address)) < 0) {
        fprintf(stderr, "bind failed\n");
        return 1;
    } // end if

    struct sockaddr_in sender_address;
    ssize_t n;
    socklen_t len;
    len = sizeof(sender_address);  //len is value/result 
    
    char buffer[1024] = { 0 };
    n = recvfrom(sockfd, (char *)buffer, 1024, MSG_WAITALL, ( struct sockaddr *) &sender_address, &len); 
    buffer[n] = '\0'; 
    printf("Client : %s\n", buffer); 

    close(sockfd);
} // end main