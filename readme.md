## Generating Recursion Tree SVG
Generate recursion tree using this program from level order traversal (breadth order traversal).

Paste your Pushbullet access_token in a file named `access_token.txt` to generate a public link which can be used to embed the SVG anywhere.

### Example
Enter the bread order traversal with each element in a new line in `inp.txt` file.
For eg. for the following breadth traversal 
`[1, 2, 3, 'null', 5, 6, 7, 'null', 9, 'null', 'null', 12, 13, 14, 15, 'null', 'null', 'null', 19, 20, 21, 'null', 23, 'null', 25]`
Following will be generated
#### Pretty-Print Tree
```text
│                   ┌── 25
│               ┌── 19
│           ┌── 13
│       ┌── 7
│       │   └── 12
│   ┌── 3
│   │   └── 6
└── 1
    │               ┌── 23
    │           ┌── 15
    │       ┌── 9
    │       │   │   ┌── 21
    │       │   └── 14
    │       │       └── 20
    │   ┌── 5
    └── 2
```
#### SVG and PNG
![alt-text](https://g.gravizo.com/source/svg/custom_mark10?https%3A//dl3.pushbulletusercontent.com/suQwFdDxR3d9fG4P3zClCfttXzbL3t75/graph_data.txt)
### Features
- Recursion Tree can also be made for strings instead of numbers.
- Returns a link to the uploaded SVG which can be used anywhere.
- Saves the generated SVG file locally.
- Outputs the graph data in [DOT Graph Description Language](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) which can be used with [GraphViz.org](https://www.graphviz.org/).
- Gives a pretty print of the tree such as shown below
```text
Breath Order Traversal - [1, 2, 3, 'null', 5, 6, 7, 'null', 9]
│       ┌── 7
│   ┌── 3
│   │   └── 6
└── 1
    │       ┌── 9
    │   ┌── 5
    └── 2
```
- Code is scalable ie. it can generate large graphs as well.
- Time Complexity : ${O}(n)$ 
- Space Complexity : ${O}(n)$
where n = number of nodes

#### Requirements
- `numpy`
- `requests`
