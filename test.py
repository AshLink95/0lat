import subprocess
import zmq
from threading import Thread
from time import sleep

# Build and run functions
def build(out1: str, out2: str) -> tuple[str, str, bool]:
    grace = True
    try:
        subprocess.run(["scons", "out1="+out1, "out2="+out2], stdout=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError as e:
        grace = False
        print(f"Couldn't build and Got the error {e}")
    return (out1, out2, grace)

def run(file: str) -> None:
    subprocess.run(["./"+file])

# Shut down sequence initiator
def close(socket: zmq.SyncSocket, client: str) -> None:
    socket.send_string("Out!")
    print(client," requesting shutdown! sending code: Out!")

output = build("server", "logger")
if output[2]:
    # System startup
    server = Thread(target=run, args=(output[0],), daemon=True)
    logger = Thread(target=run, args=(output[1],), daemon=True)
    server.start()
    logger.start()
    sleep(0.1)

    # Tests
    context = zmq.Context()

    ## Test 1
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://localhost:5555")

    send = "Hello! This is Client Py 1, reporting from Base!!"
    socket1.send_string(send)
    print("Client Py 1 Sent: "+send)

    reply = socket1.recv_string()
    print(f"Client Py 1 Received: {reply}")

    send = "My squad and I got separated. Enemy base ahead."
    socket1.send_string(send)
    print("Client Py 1 Sent: "+send)

    reply = socket1.recv_string()
    print(f"Client Py 1 Received: {reply}")

    socket1.close()

    ## Test 2
    socket2 = context.socket(zmq.REQ)
    socket2.connect("tcp://localhost:5555")

    send = "Hello! This is Client Py 2, am I calling Base?"
    socket2.send_string(send)
    print("Client Py 2 Sent: "+send)

    reply = socket2.recv_string()
    print(f"Client Py 2 Received: {reply}")

    send = "Ok, thank you! Py 2 will stand by!"
    socket2.send_string(send)
    print("Client Py 2 Sent: "+send)

    reply = socket2.recv_string()
    print(f"Client Py 2 Received: {reply}")

    ## Test 3
    socket3 = context.socket(zmq.REQ)
    socket3.connect("tcp://127.0.0.1:5555")
    send = "Hello! This is Client Py 1. Connection got intercepted!"
    socket3.send_string(send)
    print("Client Py 1 Sent: "+send)

    reply = socket3.recv_string()
    print(f"Client Py Received: {reply}")
    send = "Py 2 to Base, I eliminated the enemy camp with Py 3 and Py 4. 3 is injured."
    socket2.send_string(send)
    print("Client Py 2 Sent: "+send)

    reply = socket2.recv_string()
    print(f"Client Py Received: {reply}")
    send = "Py 1 to Base, I heard fire and saw my squad's signal from the camp. Going in."
    socket3.send_string(send)
    print("Client Py 1 Sent: "+send)
    reply = socket3.recv_string()
    print(f"Client Py 1 Received: {reply}")

    send = "I just saw my squad. Area clear. Will initiate shut down sequence once on board."
    socket3.send_string(send)
    print("Client Py 1 Sent: "+send)
    reply = socket3.recv_string()
    print(f"Client Py 1 Received: {reply}")

    send = "Py 2 to Base. Py 1 is safe. Heading to Base!"
    socket2.send_string(send)
    print("Client Py 2 Sent: "+send)
    reply = socket2.recv_string()
    print(f"Client Py 2 Received: {reply}")
    socket2.close()

    ### System shut down request
    close(socket3, "Client Py 1")
    socket3.close()

    # Disconnet client
    context.destroy()
    print("Context Down! Agent codename Client Py returned to base safely!")


# subprocess.run(["scons", "-c", "out2=logger"], stdout=subprocess.DEVNULL, check=True)
