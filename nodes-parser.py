import json
import sys
import getopt

def generate_ipaddr_json(node_file):
    node_ip_map = {}
    with open(node_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:  # Ensure the line has at least two parts
                name = parts[-1].strip('/')  # Extract the container/node name
                ip = parts[0]  # Extract the IP address
                node_ip_map[name] = ip
    
    # Write the dictionary to ipaddr.json
    with open("ipaddr.json", "w") as f:
        json.dump(node_ip_map, f, indent=4)

def main(argv):
    node_file = ''
    try:
        opts, args = getopt.getopt(argv, "n:", ["nodeFile="])
    except getopt.GetoptError:
        print("Usage: python script.py -n <nodefile>")
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ("-n", "--nodeFile"):
            node_file = arg
    
    if not node_file:
        print("Node file path is required.")
        sys.exit(2)
    
    generate_ipaddr_json(node_file)

if __name__ == "__main__":
    main(sys.argv[1:])
