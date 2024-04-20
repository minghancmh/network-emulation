import argparse 

import sender
from const import PORT, LOG_FILE_PATH


def start_sender(args):
    print("sender initializing...")
    if args.msg == None: return
    with open(args.msg, "r") as f:
        message = f.read()
    senderNode = sender.Sender(float(args.redundancy_factor), "1.1.1.1", args.dest_ip, PORT, PORT)
    with open(LOG_FILE_PATH, "a") as f:
            f.write(f"Redundancy Factor:{senderNode.redundancy_factor} ")
    msgID = senderNode.setMessage(message)
    print("[start_sender]: destination_ip: ", args.bgrip)
    senderNode.send(args.bgrip, msgID)
    print(senderNode.getkm())




# CLI setup
def main():
    parser = argparse.ArgumentParser(description='Send or listen for messages.')
    parser.add_argument('--bgrip', help="Border Gateway Router IP address (required if --nodeType is sender)")
    parser.add_argument('--dest_ip', help='Destination IP address')
    parser.add_argument('--msg', help='Message to send (required if --send is used)')
    parser.add_argument('--redundancy_factor')
    args = parser.parse_args()

    assert args.redundancy_factor != None, "Redundancy factor is required."
    print("[start_sender]:redundancyFactor: ", args.redundancy_factor)

    # 0 and "1.1.1.1" are placeholder values to be set later
    start_sender(args)

if __name__ == '__main__':
    main()
