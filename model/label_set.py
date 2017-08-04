

class LabelSet():
    def __init__(self,name):
        self.name=name
        self.num_labels = 0
        #self.labels = []
        self.populate()

    """ Initializes object labels """
    def populate(self):
        raise NotImplementedError("Base class")

    """ Returns a set of indices in range [0,len(labels)] that represent labels that should
    receive activation """
    def extract_labels_from_text(self, text):
        raise NotImplementedError("Base class")

    def __len__(self):
        return len(self.labels)

class TechniqueLabelSet(LabelSet):
    def __init__(self,):
        LabelSet.__init__(self,"technique label set")
        # Maps a technique string to an index in the label set
        self.technique_map = {}

    def populate(self):
        print("  Building technique lists...")
        i,mapped = 0,{}
        techs = base_techniques

        # Map the manual_techniques to integers
        for outer in techs:
            this_exemplar = outer[0]
            mapped[this_exemplar] = i
            for inner in outer:
                mapped[inner] = i
            mapped[this_exemplar] = i
            i+=1

        cc_loader = loader.CodechefLoader()
        for item in cc_loader.load_all():
            if "preqrequisites" in item['editorial']:
                for prereq in item['editorial']['prerequisites'].split(","):
                    prereq = prereq.strip().lower()
                    if prereq not in exemplars:
                        exemplars[prereq] = prereq
                        mapped[prereq] = i
                        i+=1

        self.num_labels = i
        print("   Done, with %d (%d) labels."%(i,len(mapped)))
        self.technique_map = mapped

    def extract_labels_from_text(self, text):
        relevant_techs = []
        for outer in techs:
            for kv in self.technique_map.items():
                if kv.key() in txt:
                    relevant_techs.append(kv.value())
        return relevant_techs


"""
    Each outer list is an equivalence class of techniques
"""
# First split on '\n' then on '.' to get list of lists
manual_techniques = """max-flow.max flow
bipartitie-matching.bipartite matching
lca.least common ancestor
binary search
dynamic programming.dp
fft.fast fourier transform.fourier transform.dft
cartesian tree.treap
heavy-light decomposition.hld.heavy light decomposition.link-cut.linkcut.link cut
segment tree.segment-tree.lazy propagation.segment trees
""".split("\n")
base_techniques = []
for outer in manual_techniques:
    inners = outer.split(".")
    inners = map(str.strip, inners)
    base_techniques.append(inners)
