import whoosh
from index import Index, Builder, TermFreq, DocVector
from matplotlib import pyplot

# def allTermsStat(collection): #As parameter p I should pass all the collection of documents
#     all_term_vec = []

#     for d in doc_id:           #-> here I need a for that slides all the documents that I have
#         all_term_vec += doc_vector(doc_id)
#     all_term_vec.sort([1]) #I'm ordering the array based on the value of TermFreq that is the element [1], elem[0] in should be the term (ascendant)
#     all_term_vec.reverse() #I invert the order so now is descendant
#     return all_term_vec()  #expected structure of the vector [(term1, freq1), (term2, freq2),..,(termN, freqN)] where freq1>freq2>..>freqN

# def allDocStat(p):
#     vec = allTermsStat(p)  #p is the collection of documents
#     i = 0
#     inDocAppearance = []
#     while i<len(vec):
#         inDocAppearance[i] = total_freq(vec[i][0]) #with vec[i] I access the tuple [term, frequency] , with i[0] I access the term
#         inDocAppearance[i].append(vec[i][0])    #I associate the number of doc where a term appears, with the term itself
#         i += 1
#     inDocAppearance.sort([1]) #I'm ordering the array based on the file [1] that should be N° of documents (ascendant)
#     inDocAppearance.reverse() #I invert the order so now is descendant
#     return inDocAppearance #expected structure of the vector [(term1, nDoc1), (term2, nDoc2),..,(termN, nDocN)] where nDoc1>nDoc2>..>nDocN

def term_stats_sort(index):
    stats = index.all_terms_with_freq()
    stats.sort(key=lambda tup: tup[1], reverse=True)

    return stats

def term_stats_docs(index):
    stats = []
    for term in index.all_terms():
        stats.append([term , index.doc_freq()])
    
    return stats

def term_stats(index):
    plotx = term_stats_sort(index)

    ploty = term_stats_docs(index)

    # pyplot.plot(plotx, ploty, )
