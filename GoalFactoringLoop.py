import networkx as nx

class GoalEngine(object):
    ROOT_NODE = 0
    def __init__(self):
        self.dg = nx.DiGraph()
        self.dg.add_node(self.ROOT_NODE)
        self.current_node  = self.ROOT_NODE
        self.history_stack = [self.ROOT_NODE]
        self.goal_stack    = []
        # self.completer = MyCompleter(self.dg.nodes())

    def addGoalToStack(self, node):
        self.goal_stack.append(node)

    def popGoals(self):
        self.dg.add_edges_from([(self.current_node, n) for n in self.goal_stack])
        self.history_stack += self.goal_stack
        self.goal_stack = []
        self.current_node = self.history_stack.pop()
        
    def run(self):
        while True:
            # Clear Output in Console (will not work in IDLE)
            cls()
            # Print Output
            if(self.goal_stack != []):
                print("Current Goal Level:\n  %s" % "\n  ".join(self.goal_stack))
            
            # Get User Input
            if(self.current_node == self.ROOT_NODE):
                message = "What do you do? "
            else:
                message = "Why do you do %s? " % self.current_node
            inp = input(message)
            
            # Check if a user control is initialized
            if(inp == ""):
                self.popGoals()
                # self.refreshCompleter()
                if(self.current_node == self.ROOT_NODE):
                    print("You're done here.")

                    break
            else:
                self.addGoalToStack(inp)

        # ROOT_NODE is junk, take it out               
        self.dg.remove_node(self.ROOT_NODE)
        return self.dg

class GraphToOrg(object):
    TaskFormat = "* %s\n :PROPERTIES:\n :task_id: %s\n :BLOCKER: %s\n :END:"
    
    def __init__(self):
        self.taskList = []

    def itemFormat(self, item):
        # org 'task_id's are space delimited, so we need to give them underscores instead
        # additionally we need to handle the case when the values given are, say, numbers, and not strings.
        return "_".join(str(item).split(" ")).lower()
    
    def org(self, graph):
        # Use the Adjacency List Format to streamline this task.
        # TODO: Use hashes for 'task_id's?
        self.taskList = [self.TaskFormat % (i[0], "".join(map(self.itemFormat, i[0])), " ".join(map(self.itemFormat, i[1]))) for i in list(((adj[0],[i[0] for i in adj[1].items()]) for adj in graph.adjacency_iter()))]       
        return "\n".join(self.taskList)

# UTILITY METHOD
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Goal Process
ge = GoalEngine()
# Export to Org
converter = GraphToOrg()

# Run the processes
goal_graph = ge.run()

# Output to file
cls()
if(input("Write out an org file (Y/y/Yes/yes)? ") in ["y", "Yes", "yes", "Y"]):
    f = open("%s.org" % input("Org File Name? "), 'w')
    f.write(converter.org(ge.dg))
    f.close()
    
if(input("Write out a GML file (Y/y/Yes/yes)? ") in ["y", "Yes", "yes", "Y"]):
    nx.write_gml(ge.dg, "%s.gml" % input("GML File Name? "))
