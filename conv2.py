import sys, numpy as np
from collections import defaultdict
from queue import Queue
import json
import requests
from urllib.parse import urlencode, quote

with open("access_token.txt") as f: ACCESS_TOKEN = f.read()
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def stringToTreeNode(inputValues):
    # print(input)
    # input = input.strip()
    # input = input[1:-1]
    # if not input:
    #     return None

    # inputValues = [s.strip() for s in input.split(',')]
    root = TreeNode(int(inputValues[0]))
    nodeQueue = [root]
    front = 0
    index = 1
    while index < len(inputValues):
        node = nodeQueue[front]
        front = front + 1

        item = inputValues[index]
        index = index + 1
        if item != "null":
            leftNumber = int(item)
            node.left = TreeNode(leftNumber)
            nodeQueue.append(node.left)

        if index >= len(inputValues):
            break

        item = inputValues[index]
        index = index + 1
        if item != "null":
            rightNumber = int(item)
            node.right = TreeNode(rightNumber)
            nodeQueue.append(node.right)
    return root

def prettyPrintTree(node, prefix="", isLeft=True):
    if not node:
        print("Empty Tree")
        return

    if node.right:
        prettyPrintTree(node.right, prefix + ("│   " if isLeft else "    "), False)

    print(prefix + ("└── " if isLeft else "┌── ") + str(node.val))

    if node.left:
        prettyPrintTree(node.left, prefix + ("    " if isLeft else "│   "), True)

def get_link(graph_data):
    with open("graph_data.txt", "w") as f: f.write(graph_data)

    resp = requests.post('https://api.pushbullet.com/v2/upload-request', data=json.dumps({'file_name': 'graph_data.txt'}), headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
    r = resp.json()
    resp = requests.post(r['upload_url'], data=r['data'], files={'file': open('graph_data.txt', 'rb')})
    print(json.dumps(r, indent = 4))
    return r['file_url']


def generate_data(value_mappings, relation_mappings, mp):
    relation_mappings_str = ',\n,'.join(relation_mappings)
    value_mappings=  [f'''{node_name} [label = "{mp[value_mappings[node_name]]}"]''' for node_name in value_mappings]

    graph_body = ";\n".join(value_mappings + relation_mappings)
    print(graph_body)
    graph_data = f'''
<details> 
<summary></summary>
custom_mark10
digraph G {{
{graph_body}
}}
custom_mark10
</details>
'''
    return graph_data


def main():

    n = int(input())
    inputValues = np.arange(1, 2**n).tolist()
    root = stringToTreeNode(inputValues)
    prettyPrintTree(root)
    # with open("inp.txt", "w") as f:
    #     f.write('\n'.join([str(i) + ":" for i in range(1, 2**n)]))

    # input()
    with open("inp.txt", "r") as f:
        lines = f.read().split('\n')

    mp = defaultdict(str)
    mp["null"] = "null"
    inputValues=  np.arange(1, len(lines) + 1).tolist()
    for ind, line in enumerate(lines):
        # ind, val = int(line[:line.index(":")].strip()), line[line.index(":") + 1:].strip()
        val = line.strip()
        mp[ind + 1] = val
        if val == "null":
            inputValues[ind] = "null"

    print(inputValues)
    root = stringToTreeNode(inputValues)
    prettyPrintTree(root)

    q = Queue(maxsize = 2**n)
    q.put(root)
    q.put("$")
    curr_val = 0
    curr_level = 0
    next_level_val = 0
    relation_mappings = []
    value_mappings = {}
    while q.qsize != 1:
        node = q.get()
        if type(node)==str and q.qsize() == 0:
            break
        if type(node)==str:
            q.put("$")
            curr_level += 1
            curr_val = 0
            null_count = 0
            next_level_val = 0
            continue
        
        curr_node_name = f"level_{curr_level}_val_{curr_val}"
        value_mappings[curr_node_name] = node.val
        # if node.val == :
        #     print('\n'.join(mappings))
        next_left_name = f"level_{curr_level + 1}_val_{next_level_val}"
        next_right_name = f"level_{curr_level + 1}_val_{next_level_val + 1}"
        if node.left and node.right:
            relation_mappings += [f"{curr_node_name} -> {{ {next_left_name} ; {next_right_name} }}"]
            next_level_val += 2
        elif node.left and not node.right:
            null_obj_name = f"null_level_{curr_level+1}_val_{null_count}"
            value_mappings[null_obj_name] = "null"
            null_count += 1
            relation_mappings += [f"{curr_node_name} -> {{ {next_left_name} ; {null_obj_name}}}"]
            next_level_val += 1
        elif not node.left and node.right:
            null_obj_name = f"null_level_{curr_level+1}_val_{null_count}"
            value_mappings[null_obj_name] = "null"
            null_count += 1
            next_right_name = f"level_{curr_level + 1}_val_{next_level_val}"
            relation_mappings += [f"{curr_node_name} -> {{ {null_obj_name} ; {next_right_name} }}"]
            next_level_val += 1
        
        if node.left:
            q.put(node.left)
        if node.right:
            q.put(node.right)

        curr_val += 1

    print(",\n".join(relation_mappings))
    print(json.dumps(value_mappings, indent = 4))
    print(json.dumps(mp, indent = 4))

    graph_data = generate_data(value_mappings, relation_mappings, mp)
    return
    graph_link = get_link(graph_data)
    print(graph_link)
    encoded_url = quote(graph_link)
    final_url = "https://g.gravizo.com/source/svg/custom_mark10?" + encoded_url
    print(final_url)
    # relation_mappings_str = '\n'.join(relation_mappings)
    # value_mappings_str = '\n'.join([f"{node_name} = {mp[value_mappings[node_name]]}" for node_name in value_mappings])
    # print(value_mappings_str)

if __name__ == '__main__':
    main()    