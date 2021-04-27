from ipaddress import IPv4Network

def get_object_groups(config):
    object_group_indicies = list()
    for i in range (len(config)):
        if config[i].strip().startswith("object"):
            object_group_indicies.append(i)
    
    object_groups = list()
    prev_index = 0
    for index in object_group_indicies:
        if index != 0:
            object_groups.append(config[prev_index:index])  # Get the slice of object-group
            prev_index = index                              # Next object-group starts here
    object_groups.append(config[prev_index:] )          # Get the final object-group

    return object_groups

def normalize_obj_group(object_groups):
    normalized_obj_groups = []
    for obj_group in object_groups:
        if obj_group[0].startswith('object-group network'):
            normalized_obj_groups.append(normalize_network_obj_grp(obj_group))
        elif obj_group[0].startswith('object-group port'):
            normalized_obj_groups.append(normalize_port_obj_group(obj_group))

    return normalized_obj_groups

def normalize_port_obj_group(object_group):
    # object-group service TEST tcp-udp
    # port-object eq ftp
    # port-object range range 1024 4500
    new_obj_grp = []
    for line in object_group:
        if line.strip().startswith("!"):
            continue
        elif line.strip().startswith('object-'):
            line = object_group[0].replace(' port ', ' service ') + " tcp-udp"
        elif line.strip().startswith('range'):
            line = "port-object " +  line
        elif line.strip().startswith('eq'):
            line = "port-object " + line
        new_obj_grp.append(line)
    return new_obj_grp

def normalize_network_obj_grp(object_group):
    new_obj_grp = []
    for line in object_group:
        if line.strip().startswith("!"):
            continue
        elif line.startswith('object-'):
            line = object_group[0].replace(' ipv4 ', ' ')
            new_obj_grp.append(line)
        else:
            network = str(IPv4Network(line).network_address)
            subnet = str(IPv4Network(line).netmask)
            new_obj_grp.append(f"network-object {network} {subnet}")
    return new_obj_grp

if __name__ == "__main__":
    raw_config = []
    with open('ipv4.csv', "r", encoding='utf-8-sig') as file_object:
        for line in file_object :
    	    raw_config.append(line.strip())

    raw_object_groups = get_object_groups(raw_config)
    object_groups = normalize_obj_group(raw_object_groups)

    print("! Conversion Output !")
    for obj_grp in object_groups:
        for line in obj_grp:
            print(line)
        print("!")




        

