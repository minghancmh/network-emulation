import argparse 

import const, sender, receiver, router


# CLI setup
def main():
    parser = argparse.ArgumentParser(description='Send or listen for messages.')
    parser.add_argument('--nodeType', help="Type of node (sender or receiver or router)", required=True)
    # parser.add_argument('--send', action='store_true', help='Send message')
    parser.add_argument('--dest_ip', help='Destination IP address (required if --send is used)')
    parser.add_argument('--msg', help='Message to send (required if --send is used)')
    parser.add_argument('--port', default=const.PORT, type=int, help='Destination port (default: 10000)')
    parser.add_argument('--listen', action='store_true', help='Start listening for messages')
    args = parser.parse_args()
    assert args.nodeType in ["sender", "receiver", "router"], "Invalid node type. Must be sender, receiver, or router."

    if args.nodeType == "router":
        print("Router node not yet implemented.")
        return
    elif args.nodeType == "sender":
        # 0 and "1.1.1.1" are placeholder values to be set later
        print("sender not implemented")
        # senderNode = sender.Sender(0, args.msg, "1.1.1.1", args.dest_ip, args.port, args.port)
        # senderNode.send(args.dest_ip, args.msg)
    elif args.nodeType == "receiver":
        # all placeholder values to be set later
        receiverNode = receiver.Receiver("1.1.1.1")
        print("Node listening for messages...\n")
        receiverNode.recv()


    else:
        parser.print_help()

if __name__ == '__main__':
    main()
