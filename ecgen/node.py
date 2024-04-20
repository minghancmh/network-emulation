import argparse 

import const, sender, receiver, router

from multiprocessing import Process
import os
import time

from const import LOG_FILE_PATH, PACKET_DROP_RATE

def infinite_loop():
    while True:
        time.sleep(10) # defensively yield processor 

def start_sender(args):
    print("sender initializing...")
    if args.msg == None: return
    with open(args.msg, "r") as f:
        message = f.read()
    senderNode = sender.Sender(0.2, "1.1.1.1", args.dest_ip, args.port, args.port)
    msgID = senderNode.setMessage(message)
    senderNode.send(args.bgrip, msgID)
    print(senderNode.getkm())


def startRouter(args):
    print("router initializing...with args:",args)
    routerNode = router.Router(float(PACKET_DROP_RATE))
    # routerNode = router.Router(0)
    with open(LOG_FILE_PATH, "a") as f:
            f.write(str(f"Drop Rate:{routerNode.probabilityDropRate} "))
    print("router initialized")


# CLI setup
def main():
    parser = argparse.ArgumentParser(description='Send or listen for messages.')
    parser.add_argument('--nodeType', help="Type of node (sender or receiver or router)", required=True)
    parser.add_argument('--bgrip', help="Border Gateway Router IP address (required if --nodeType is sender)")
    parser.add_argument('--dest_ip', help='Destination IP address')
    parser.add_argument('--msg', help='Message to send (required if --send is used)')
    parser.add_argument('--port', default=const.PORT, type=int, help='Destination port (default: 10000)')
    parser.add_argument('--listen', action='store_true', help='Start listening for messages')
    parser.add_argument('--router_drop_rate')
    args = parser.parse_args()
    assert args.nodeType in ["sender", "receiver", "router"], "Invalid node type. Must be sender, receiver, or router."



    if args.nodeType == "router":
        print("[node.py]: router_drop_rate=", args.router_drop_rate)

        assert args.router_drop_rate != None, "Router drop rate is required."
        assert float(args.router_drop_rate) >= 0 and float(args.router_drop_rate) <= 1, "Router drop rate must be between 0 and 1."

    while not os.path.exists('/app/routing_tables.json'):
        print("Waiting for the ipaddr and routing_tables to be loaded into container...")
        time.sleep(2) # MUST NOT BE REMOVED! This is a "synchonization" mechanism to ensure that the routing tables are loaded into the container before the router starts.
    while not os.path.exists('/app/ipaddr.json'):
        print("Waiting for the ipaddr and routing_tables to be loaded into container...")
        time.sleep(2) # MUST NOT BE REMOVED! This is a "synchonization" mechanism to ensure that the ipaddr.json are loaded into the container before the router starts.

    if args.nodeType == "router":
        print("router initializing...")
        proc = Process(target=infinite_loop)
        proc2 = Process(target=startRouter, args=(args,))
        proc.start()
        proc2.start()


    elif args.nodeType == "sender":
        # 0 and "1.1.1.1" are placeholder values to be set later
        process1 = Process(target=start_sender, args=(args,))
        process2 = Process(target=infinite_loop)
        process1.start()
        process2.start()
        print("both processes started")

    elif args.nodeType == "receiver":
        # all placeholder values to be set later
        receiverNode = receiver.Receiver("1.1.1.1")
        print("Node listening for messages...\n")
        receiverNode.recv()


    else:
        parser.print_help()

if __name__ == '__main__':
    main()
