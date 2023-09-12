import time
import colorama
from colorama import Fore

colorama.init()

def equal_set_minimum(equal_marking_sets):
    min_element = min([min(marking_set) for marking_set in equal_marking_sets]) # minimum element across sets
    min_element_count = [element.count(min_element) for element in equal_marking_sets]
    return equal_marking_sets[min_element_count.index(max(min_element_count))]
     

def minimum_initial_marking(initial_marking_sets):
        ims_sum = [sum(ims) for ims in initial_marking_sets] #ims stands for initial marking set
        min_sum = min(ims_sum)
        if ims_sum.count(min_sum) == 1:
            minimum_set = initial_marking_sets[ims_sum.index(min_sum)]
            return minimum_set
        else:
            equal_sets = [i for i in initial_marking_sets if sum(i) == min_sum]
            minimum_set= equal_set_minimum(equal_sets)
            return minimum_set

class FiringSequence:
    def __init__(self, sequence, places):
        self.sequence = sequence
        self.initial_marking = dict()
        for place in places:
            self.initial_marking[place.label] = 0

    def __str__(self):
        return f'Firing Sequence: {self.sequence}'
    
        
class Place:
    def __init__(self, label=None):  # Holding is the amount of tokens
        self.label = label 
        self.holding = 0

    def __str__(self):
        return f'{self.label} Holding -> {self.holding} Tokens'
    
    def reset_holding(self):
        self.holding = 0

class ArcBase:
    def __init__(self, place, amount=1): # amount is the amount the arc adds to a place depending if it's incoming or outgoing
        self.place = place
        self.amount = amount

class Out(ArcBase):
    def trigger(self): 
        self.place.holding -= self.amount

    def non_blocking(self):
        return self.place.holding >= self.amount
    
    def blocking(self):
        return self.place.holding < self.amount
    
    def mark_blocking(self, firing_sequence):
        self.place.holding += 1
        firing_sequence.initial_marking[self.place.label] +=1
     
class In(ArcBase):
    def trigger(self):
        self.place.holding += self.amount

class Transition:
    def __init__(self, out_arcs, in_arcs, label=None):
        self.label = label
        self.out_arcs = set(out_arcs)
        self.arcs = self.out_arcs.union(in_arcs)

    def fire(self, firing_sequence):
        for arc in self.out_arcs:
            if arc.blocking():
                arc.mark_blocking(firing_sequence)

        for arc in self.arcs:
            arc.trigger()
    
    def __str__(self):
        return self.label

class PetriNet:
    def __init__(self, transitions, places):
        self.transitions = transitions
        self.places = places

    def run(self, firing_sequence):
        print(Fore.YELLOW + "Using firing sequence: " + " => ".join(firing_sequence.sequence) + "\n")
        # print("start {}\n".format([p.holding for p in self.places]))

        for name in firing_sequence.sequence:
            t = self.transitions[name]
            print(Fore.WHITE + "Sequence {} firing!".format(name))
            time.sleep(0.5)
            t.fire(firing_sequence)
            
            print(" => {}\n".format([p.holding for p in self.places]))
            time.sleep(0.5)

        print(Fore.BLUE + "Final state:  {}\n".format([p.holding for p in self.places]))
        print(f"Initial marking: {firing_sequence.initial_marking}\n")

if __name__ == "__main__":

    # Draw the petri net
    ps = [Place(f'P{i}') for i in range(1, 5)]
    ts = dict(
        t1 = Transition([Out(ps[0])], [In(ps[1])], 'T1'),
        t2 = Transition([Out(ps[1])], [In(ps[2])], 'T2'),
        t3 = Transition([Out(ps[2])], [In(ps[1])], 'T3'),
        t4 = Transition([Out(ps[1])], [In(ps[3])], 'T4'),
    )

    # while True:
    #     labeling_sequence = input("Input labeling sequence: ")

    #     if len(labeling_sequence) == len(ts) and labeling_sequence.isalpha():
    #         break
    #     else:
    #         print("Invalid labeling sequence. Try again.")

    # Instantiate the petri net object
    petri_net = PetriNet(ts, ps)

    # Hardcoded firing sequences: to be replaced with
    # firing sequences generated from labeling sequence
    firing_sequences = [['t1', 't1', 't3', 't4'], 
                        ['t1', 't2', 't3', 't4'],
                        ['t2', 't1', 't3', 't4'],
                        ['t2', 't2', 't3', 't4'],]

    # Instantiate the firing sequences
    fs = [FiringSequence(sequence, ps) for sequence in firing_sequences]
    
    initial_marking_sets = []

    for firing_sequence in fs:
        petri_net.run(firing_sequence)
        initial_marking_sets.append(tuple(firing_sequence.initial_marking.values()))
        
        time.sleep(0.5)
        print(Fore.RED + "Resetting tokens all tokens to 0\n")
        print(Fore.WHITE + "---------------------------------\n")
        for place in ps:
            place.reset_holding()
    
    print(f'The initial marking sets: {initial_marking_sets}\n')
    print(Fore.GREEN + f'The minimum initial marking is: {minimum_initial_marking(initial_marking_sets)}')




