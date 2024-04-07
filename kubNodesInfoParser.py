import json
import getopt
import sys

def main(argv):
    nodefile = ''
    try:
        opts, args = getopt.getopt(argv[1:], "n:", ["nodeFile="])
    except getopt.GetoptError:
        print("getopt error")
        sys.exit(1)
        
    for opt, arg in opts:
        if opt in ("-n", "--nodeFile"):
            nodefile = arg
    with open(nodefile, "r") as f:
        data = f.read()

    # Split the data into lines for processing
    lines = data.strip().split('\n')

    # Initialize an empty dictionary to hold the mappings
    node_ip_map = {}

    # Iterate over each line after the header
    for line in lines[1:]:
        parts = line.split()
        # Assuming the NAME is the first part and INTERNAL-IP is the sixth part
        name, internal_ip = parts[0], parts[5]
        node_ip_map[name] = internal_ip


    with open("ipaddr.json", "w") as f:
        json.dump(node_ip_map, f)
        
if __name__ == "__main__":
    main(sys.argv)
        



