import json
import requests
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph):

    # create networkx graph
    G=nx.Graph()
    numEdges = 0
    numNodes = 0
    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])
        numEdges = numEdges + 1
        G.add_nodes_from([edge[0], edge[1]])
    
    d = nx.degree(G)
    numNodes = len([i for i in dict(d).values()])
    maxDegree = max([i for i in dict(d).values()])
    maxDegreeNode = ""
    for node, degree in dict(d).items():
        if degree == maxDegree:
            maxDegreeNode = "" + node
    firstURL = "https://blockchain.info/rawaddr/"
    request = firstURL + maxDegreeNode
    jsonRequest = (requests.get(request)).json()
    print("Num of nodes in graph:" + str(numNodes) + "\n" + "Num of edges in graph:"+ str(numEdges))
    print ("\ntotal_received:" + str(jsonRequest["total_received"]) + "\n" + "total_sent:" + str(jsonRequest["total_sent"]) + "\n"+"final_balance:" + str(jsonRequest["final_balance"]))
    nx.draw(G,node_size=[v/10 for v in dict(d).values()])
    # show graph
    plt.savefig("graph.png")
    plt.show()



firstpart = "https://blockchain.info/rawaddr/"
#initialinput = input("please type the 'seed' address: ")
initialinput = "18NzmGzcY9HsWsQdr5PmmTTYoX1GuCqJu9"
initialreq = firstpart + initialinput

firstjson = (requests.get(initialreq)).json()
graphvizlines = []

addresslist = []
usedaddresslist = []

addresslist.append(initialinput)
usedaddresslist.append(initialinput)

z = 0
i = 0
graph = []
# we need to monitor the latest block and get the transaction hash with highest number of transactions in graph
# Take the input address in the transaction and take that as seed address for below part
while i < 6:
    if z is 1:
        initialreq = firstpart + addresslist[i]
        firstjson = (requests.get(initialreq)).json()

    for transaction in firstjson["txs"]:
        payerlist = []
        recipientlist = []

        #print("\n" + transaction["hash"])

        for item in transaction["inputs"]:
            payerlist.append(item["prev_out"]["addr"])
            if item["prev_out"]["addr"] not in addresslist:
                addresslist.append(item["prev_out"]["addr"])

        for target in transaction["out"]:
            recipientlist.append(target["addr"])
            if target["addr"] not in addresslist:
                addresslist.append(target["addr"])

        for payer in payerlist:
            for recipient in recipientlist:
                a = '"' + payer + '"' + " -> " + '"' + recipient + '"' + ";"
                if a not in graphvizlines:
                    graphvizlines.append(a)
                    graph.append((payer,recipient))

    i = i + 1
    z = 1


for t in graphvizlines:
    print(t)

# if edge labels is not specified, numeric labels (0, 1, 2...) will be used
draw_graph(graph)
