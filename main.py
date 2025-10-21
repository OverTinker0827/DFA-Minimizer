
import sys
from collections import deque,defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import argparse

class Minimizer:
    def __init__(self):
        self.dfa={
            "states":[],
            "inputs":[],
            "start_state":None,
            "final_states":[],
            "transitions":{}
        }
    def minimize(self,input_file="input.txt",output_file="output.txt",visualize=True):
            self.read_file(input_file)

            self.process()
     
            self.write_file(output_file)
            if visualize:
                self.visualize()
    def visualize(self):

        fsm_data = self.dfa["transitions"]
        G = nx.DiGraph()
        for (src, inp), tgt in fsm_data.items():
            G.add_edge(src, tgt, label=inp)

       
        pos = nx.spring_layout(G, k=0.7, iterations=50)

        plt.figure(figsize=(12, 10))

       
        nx.draw_networkx_nodes(G, pos, node_size=1800, node_color='lightsalmon', edgecolors='black')


        nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')


        edge_groups = defaultdict(list)
        for u, v, d in G.edges(data=True):
            edge_groups[(u,v)].append(d['label'])

        for (u,v), labels in edge_groups.items():
            n = len(labels)
   
            if n == 1:
                rad_list = [0.0]
            else:
                rad_list = [0.2 + i*0.2 for i in range(n)]
       
                rad_list = [rad if i%2==0 else -rad for i, rad in enumerate(rad_list)]
            
            for rad, label in zip(rad_list, labels):
                nx.draw_networkx_edges(
                    G, pos,
                    edgelist=[(u,v)],
                    arrowstyle='-|>',
                    arrowsize=50,
                    edge_color='darkslategray',
                    connectionstyle=f'arc3, rad={rad}'
                )
  
                nx.draw_networkx_edge_labels(
                    G, pos,
                    edge_labels={(u,v): label},
                    font_color='darkred',
                    font_size=12,
                    label_pos=0.5
                )

        plt.title("Minimized DFA", fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    def process(self):
        states,inputs,start_state,final_states,transitions=self.dfa["states"],self.dfa["inputs"],self.dfa["start_state"],self.dfa["final_states"],self.dfa["transitions"]
        states=self.get_reachable_states()
        table={a:{b: 0 for b in states} for a in states}
        changes=True
    

        for a in states:
            for b in states:
                if a==b:
                    continue
                if (a in final_states)!=(b in final_states):
                    table[a][b]=1
    
        while changes:
            changes=False
            for a in states:
                for b in states:
                    if a==b or table[a][b]==1:
                        continue
                    for i in inputs:
                        a_next=transitions[(a,i)]
                        b_next=transitions[(b,i)]
                        if not a_next or not b_next:
                            continue
                        if table[a_next][b_next]==1 or table[b_next][a_next]==1:
                            table[a][b]=1
                            changes=True
                            break
        groups=[]

        visited=set()

        for a in states:
            if a in visited:
                continue
            group={a}
            visited.add(a)

            for b in states:
                if a!=b and table[a][b]==0 and table[b][a]==0:
                    group.add(b)
                    visited.add(b)
            groups.append(group)

        new_states=["".join(sorted(g)) for g in groups]
        new_transitions={}
        new_final_states=set()
        new_start_state=None
        for j in new_states:
            if start_state in j:
                new_start_state=j
                break
        fs=set(final_states)
        for i in fs:
            for j in new_states:
                if j in new_final_states:
                    continue
                if i in j:
                    new_final_states.add(j)
                    break
        for idx,s in enumerate(new_states):
            for i in inputs:
                rep=list(groups[idx])[0]
                ns=transitions.get((rep,i))
                if not ns:
                    continue
                for k in new_states:
                    if ns in k:
                        new_transitions[(s,i)]=k
                        break
        

        self.dfa["states"],self.dfa["inputs"],self.dfa["start_state"],self.dfa["final_states"],self.dfa["transitions"]=new_states,inputs,new_start_state,list(new_final_states),new_transitions


    def get_reachable_states(self):
        start_state,transitions,inputs,states=self.dfa["start_state"],self.dfa["transitions"],self.dfa["inputs"],self.dfa["states"]
        visited=set()
      

        queue=deque()
        queue.append(start_state)

        while queue:
            node=queue.popleft()
            if node in visited:
                continue
            visited.add(node)
         
            for a in inputs:
                queue.append(transitions[(node,a)])
        
        return list(visited)
    def read_file(self,filename):
        try:
            with open(filename,'r') as file:
                lines=file.readlines()
        except IOError as e:
            print(e)
            sys.exit(1)
        else:
            for idx,l in enumerate(lines):
                lines[idx]=l.strip()
            reading_transitions=False
            for l in lines:
                if reading_transitions:
                    if "=" in l:
                        reading_transitions=False
                    else:    
                        cs,inp,ns=[x.strip() for x in l.split(",")]
                        self.dfa["transitions"][(cs,inp)]=ns

                if l.startswith("states"):
                    self.dfa["states"]=[x.strip() for x in l.split("=")[1].split(",") ]
                elif l.startswith("inputs"):
                    self.dfa["inputs"]=[x.strip() for x in l.split("=")[1].split(",") ]
                elif l.startswith("start_state"):
                    self.dfa["start_state"]=l.split("=")[1].strip()
                elif l.startswith("final_states"):
                    self.dfa["final_states"]=[x.strip() for x in l.split("=")[1].split(",") ]
                elif l.startswith("transitions"):
                    reading_transitions=True
                    continue
        

    

    def write_file(self,file_path):
        states,language,start_state,final_states,transitions=self.dfa["states"],self.dfa["inputs"],self.dfa["start_state"],self.dfa["final_states"],self.dfa["transitions"]
        with open(file_path,"w") as file:
            file.write("states = "+",".join(states)+"\n")
            file.write("inputs = "+",".join(language)+"\n")
            file.write(f"start_state = {start_state}"+"\n")
            file.write("final_states = "+",".join(final_states)+"\n")
            file.write("transitions = \n")
            for a in states:
                for i in language:
                    if (a,i) in transitions:
                        ns=transitions[(a,i)]
                        file.write(",".join([a,i,ns])+"\n")



def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-i",default="input.txt")
    parser.add_argument("-o",default="output.txt")
    parser.add_argument("-v",action="store_true",default=False)
    args=parser.parse_args()
    dfa=Minimizer()
    dfa.minimize(args.i,args.o,args.v)
    
    return 

if __name__=="__main__":
    main()
