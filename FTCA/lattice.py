from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import utils

#frequent_phrases = ['information retrieval', 'natural language', 'real time', 'knowledge based', 'reinforcement learning',
#                    'large scale', 'based approach', 'problem solving', 'knowledge representation', 'model based',
#                    'case based', 'multi agent', 'web search', 'semantic web', 'semi supervised', 
#                    'object oriented', 'knowledge bases', 'constraint satisfaction', 'text classification', 'database systems',
#                    'expert systems', 'knowledge base', 'query processing', 'machine learning', 'case study',
#                    'association rules', 'constraint satisfaction problems']
#topics_phrases = [['problem solving', 'constraint satisfaction', 'constraint satisfaction problems'],
#                  ['knowledge based', 'based approach', 'knowledge representation', 'knowledge bases', 'database systems', 'expert systems', 'knowledge base'],
#                  ['natural language'],
#                  ['knowledge based', 'large scale', 'based approach', 'case based', 'machine learning', 'case study'],
#                  ['based approach','object oriented', 'query processing', 'association rules'],
#                  ['multi agent'],
#                  ['real time', 'reinforcement learning', 'machine learning'],
#                  ['information retrieval', 'based approach', 'case based', 'web search', 'semantic web', 'semi supervised', 'text classification', 'machine learning']]

class Lattice(object):
    def __init__(self, frequent_phrases, topics_phrases):
        self.frequent_phrases = frequent_phrases
        self.topics_phrases = topics_phrases
        self.topics_num = len(topics_phrases)
        self.phrases_topics = defaultdict(lambda : [])
        self.topicset_phrases = defaultdict(lambda : [])
        self.clattice = nx.DiGraph()
        self.traverse_list = list()

    
    def map_phrase_topic(self):
        topic_id = 0
        for topic in self.topics_phrases:
            for fp in self.frequent_phrases:
                if fp in topic:
                    self.phrases_topics[fp].append(topic_id)
            topic_id = topic_id + 1
        for (k, v) in self.phrases_topics.items():
            self.topicset_phrases[tuple(v)].append(k)
            #print((k,v))
    
    def init_lattice(self):

        topics_set = list()
        node_dict = defaultdict(lambda: tuple())
        # there may exist phrases belong to all topics
        if tuple(list(range(self.topics_num))) not in self.topicset_phrases.keys():
            self.clattice.add_node((tuple(list(range(self.topics_num))), tuple()))
            node_dict[tuple(list(range(self.topics_num)))] = tuple()
            topics_set.append(set(range(self.topics_num)))
        self.clattice.add_node(((), tuple()))
        node_dict[()] = tuple()
        topics_set.append(set())
        
        # add nodes into lattice graph
        for (topics, topic_phrases) in self.topicset_phrases.items():
            print((topics, topic_phrases))
            self.clattice.add_node((tuple(topics), tuple(topic_phrases)))
            node_dict[tuple(topics)] = tuple(topic_phrases)
            topics_set.append(set(topics))
        
        # build edges dependencies according to fca
        super_sub_dict = defaultdict(lambda: [])
        for sub_item in topics_set:
            for super_item in topics_set:
                if sub_item.issubset(super_item) is True and len(sub_item) < len(super_item):
                    # when super item list is empty
                    if len(super_sub_dict[tuple(sub_item)]) == 0:
                        super_sub_dict[tuple(sub_item)].append(tuple(super_item))
                    else:
                        # current super set is smaller than the top in the list
                        if len(super_item) < len(super_sub_dict[tuple(sub_item)][-1]):
                            # But the current super set is a sub set of the top, so pop 
                            if super_item.issubset(super_sub_dict[tuple(sub_item)][-1]) is True:
                                #print((sub_item,super_item))
                                #print(super_sub_dict[tuple(sub_item)])
                                super_sub_dict[tuple(sub_item)].pop()
                            super_sub_dict[tuple(sub_item)].append(tuple(super_item))
                        else:
                            if len(super_item) == len(super_sub_dict[tuple(sub_item)][-1]):
                                super_sub_dict[tuple(sub_item)].append(tuple(super_item))
        # add edges
        for (sub_item,super_items) in super_sub_dict.items():
            #print((sub_item,super_items))
            for super_item in super_items:
                self.clattice.add_edge((super_item, node_dict[super_item]),(sub_item, node_dict[sub_item]))
        
        #plt.subplot(121)
        #nx.draw(self.clattice, with_labels=True, font_weight='bold', font_size=4)
        #plt.show()
        #plt.savefig("path.png")

    def BFSTraverse(self):
        #print(self.clattice.nodes)
        top_key = tuple(list(range(self.topics_num)))
        top_node = (top_key, tuple(self.topicset_phrases[top_key]))
        traverse_result = nx.bfs_successors(self.clattice, top_node)
        #print('BFS')
        #for x in traverse_result:
            #print(x)        

frequent_phrases = utils.load_phrases()
topics_phrases = utils.load_topics(5)
#print(frequent_phrases)
#print(topics_phrases)

lattice = Lattice(frequent_phrases,topics_phrases)
lattice.map_phrase_topic()
lattice.init_lattice()
lattice.BFSTraverse()
#print(frequent_phrases)
#print(topics_phrases)

