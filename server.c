#include <zmq.h>
#include <stdlib.h>
#include <string.h>

int main (void)
{
    // Socket to talk to clients
    void* context = zmq_ctx_new();
    void* publisher = zmq_socket(context, ZMQ_PUB);
    int publish = zmq_bind(publisher, "tcp://*:5554");

    void* responder = zmq_socket(context, ZMQ_REP);
    int response = zmq_bind(responder, "tcp://*:5555");

    // Check for creation success
    if (response || publish) {
        printf("Server failure\n");
        return -1;
    } else {
        printf("Server Up!\n");
        zmq_send(publisher, "Powering up!", 12, 0);
    }

    // Server activities
    while (!response) {
        static const size_t buflen = 100;
        char buffer[buflen];
        int recv = zmq_recv(responder, buffer, buflen, 0);
        buffer[recv] = '\0';
        printf("Server Received: %s\n", buffer);

        char* log;
        size_t len = 18+recv;
        log = malloc(len);
        snprintf(log, len, "INFO  | IN     | %s", buffer);
        zmq_send(publisher, log, len, 0);
        free(log);

        if (!strcmp(buffer, "Out!")){
            printf("Roger that! Initiating shut down sequence\n");
            zmq_send(publisher, "Shutting down!", 14, 0);
            response = -1;
            continue;
        } else if (!strncmp(buffer, "LOGIN", 5)) {

        }

        static const char reply[] = "Roger from Base!";
        zmq_send(responder, reply, strlen(reply), 0);
        printf("Server Sent: %s\n", reply);

        len = 18+strlen(reply);
        log = malloc(len);
        snprintf(log, len, "INFO  | OUT    | %s", reply);
        zmq_send(publisher, log, len, 0);
        free(log);
    }

    // shut down sequence
    zmq_close(responder);
    printf("Port down! ");
    zmq_close(publisher);
    printf("Port down! ");
    zmq_ctx_destroy(context);
    printf("Server down!\n");
    return 0;
}
