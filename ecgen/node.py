import argparse 

import const, sender, receiver, router

from multiprocessing import Process

import time

def infinite_loop():
    while True:
        time.sleep(10) # defensively yield processor 

def start_sender(args):
    print("sender initializing...")
    with open(args.msg, "r") as f:
        message = f.read()
    senderNode = sender.Sender(0.2, message, "1.1.1.1", args.dest_ip, args.port, args.port)
    senderNode.send(args.bgrip)
    print(senderNode.getkm())

def startRouter():
    print("router initializing...")
    routerNode = router.Router(0)
    sendProc = Process(target=routerNode.send())
    recvProc = Process(target=routerNode.recv())
    sendProc.start()
    recvProc.start()


# CLI setup
def main():
    parser = argparse.ArgumentParser(description='Send or listen for messages.')
    parser.add_argument('--nodeType', help="Type of node (sender or receiver or router)", required=True)
    parser.add_argument('--bgrip', help="Border Gateway Router IP address (required if --nodeType is sender)")
    parser.add_argument('--dest_ip', help='Destination IP address (required if --send is used)')
    parser.add_argument('--msg', help='Message to send (required if --send is used)')
    parser.add_argument('--port', default=const.PORT, type=int, help='Destination port (default: 10000)')
    parser.add_argument('--listen', action='store_true', help='Start listening for messages')
    args = parser.parse_args()
    assert args.nodeType in ["sender", "receiver", "router"], "Invalid node type. Must be sender, receiver, or router."

    if args.nodeType == "router":
        print("router initializing...")
        proc = Process(target=infinite_loop)
        proc2 = Process(target=startRouter)
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
