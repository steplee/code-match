import numpy as np
import tensorflow as tf
import label_set

# TODO
""" I should be able to have entire SETS of labels I want to compute activations of.
For example my first idea was to have solution techniques, but I may also want other concepts
like the type of problem, difficulty, etc.
"""


class FirstModel():
    def __init__(self,
            input_emb_width,    # dimensionality of each word vector
            hidden_size,        # num hidden layers
            labelset,           # The prerequisites # TODO allow multiple sets
            input_emb):         # input embedding table
        self.label_set = labelset

    def train_one(self, brief_txt, edit_txt):
        # Note: this returns a LIST of INDICES, not a one-hot vector
        # each index is guaranteed to be < tech_set.num_labels
        on_labels = self.labelset.extract_labels_from_text(edit_txt)


def start():
    import build_embeddings
    labels = label_set.TechniqueLabelSet()
    embs = build_embeddings.build_embeddings()

    m = FirstModel(300, 100, techs, embs)

    tech_set = TechniqueLabelSet()
    import loader
    cc_loader = loader.SimpleLoader("codechef/")

    print("Beginning Training...")
    for item in cc_loader:
        # brief
        br = item['brief']
        ed = item['editorial']


        # TODO batch it
        m.train_one(br, ed)

    print("...Done training")
