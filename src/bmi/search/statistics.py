import whoosh
from whoosh import Index, Builder, TermFreq, DocVector

def allTermsStat(p) #As parameter p I should pass all the collection of documents
    all_term_vec = []
    #for d in doc_id:           -> here I need a for that slides all the documents that I have
    
        all_term_vec += doc_vector(doc_id)
    all_term_vec.sort([1]) #I'm ordering the array based on the value of TermFreq that is the element [1], elem[0] in should be the term (ascendant)
    all_term_vec.reverse()      #I invert the order so now is descendant
    return all_term_vec()