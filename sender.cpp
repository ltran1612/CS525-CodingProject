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
    struct sockaddr_in recv_addr;
    recv_addr.sin_family = AF_INET;
    recv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary
    // form
    if (inet_pton(AF_INET, "127.0.0.1", &recv_addr.sin_addr) <= 0) {
        fprintf(stderr, "Invalid address: Address not supported \n");
        return 1;
    } // end if

    // connect to the receiver
    if (connect(sockfd, (struct sockaddr*)&recv_addr, sizeof(recv_addr)) == -1) {
        fprintf(stderr, "Connection Failed\n");
        return 1;
    } // end if

    send(sockfd, "hello", strlen("hello"), 0);
    close(sockfd);
    return 0;
}