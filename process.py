


def process(states,inputs,start_state,final_states,transitions):
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
    
    print(new_states,new_start_state,list(new_final_states))
    return new_states,inputs,new_start_state,list(new_final_states),new_transitions


# states = ["A1", "B", "C", "D"]
# alphabet = ["0", "1"]
# start_state = "A1"
# accept_states = ["D","C"]
# transitions = {
#     ("A1", "0"): "B",
#     ("A1", "1"): "D",
#     ("B", "0"): "A1",
#     ("B", "1"): "C",
#     ("C", "0"): "D",
#     ("C", "1"): "D",
#     ("D", "0"): "D",
#     ("D", "1"): "D"
# }

# process(states,alphabet,start_state,accept_states,transitions)


def read_file(filename):

    with open(filename,'r') as file:
        lines=file.readlines()
    states=[]
    language=[]
    start_state=None
    final_states=[]
    transitions={}
    for idx,l in enumerate(lines):
        lines[idx]=l.strip()
    reading_transitions=False
    for l in lines:
        if reading_transitions:
            if "=" in l:
                reading_transitions=False
            else:    
                cs,inp,ns=[x.strip() for x in l.split(",")]
                transitions[(cs,inp)]=ns

        if l.startswith("states"):
            states=[x.strip() for x in l.split("=")[1].split(",") ]
        elif l.startswith("language"):
            language=[x.strip() for x in l.split("=")[1].split(",") ]
        elif l.startswith("start_state"):
            start_state=l.split("=")[1].strip()
        elif l.startswith("final_states"):
            final_states=[x.strip() for x in l.split("=")[1].split(",") ]
        elif l.startswith("transitions"):
            reading_transitions=True
            continue
    
    # print(states,language,start_state,final_states,transitions)
    return states,language,start_state,final_states,transitions

def write_file(states,language,start_state,final_states,transitions,file_path="output.txt"):
    with open(file_path,"w") as file:
        file.write("states = "+",".join(states)+"\n")
        file.write("language = "+",".join(language)+"\n")
        file.write(f"start_state = {start_state}"+"\n")
        file.write("final_states = "+",".join(final_states)+"\n")
        file.write("transitions = \n")
        for a in states:
            for i in language:
                if (a,i) in transitions:
                    ns=transitions[(a,i)]
                    file.write(",".join([a,i,ns])+"\n")



def main():


    write_file(*process(*read_file("./input.txt")))
    return 

if __name__=="__main__":
    main()
