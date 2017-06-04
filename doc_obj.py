class Documento(object):
    name = ""
    palavras = []
    score = 0
    my_rank = 0
    pubmed_rank = 0

    def __init__(self, name, text, pubmed_rank):
        self.name = name
        self.palavras = text
        self.pubmed_rank = pubmed_rank


def make_doc(name, palavras, pubmed_rank):
    doc = Documento(name, palavras, pubmed_rank)
    return doc
