"""
 Copyright (C) 2021 Pablo Castells y Alejandro Bellogín

 Este código se ha implementado para la realización de las prácticas de
 la asignatura "Búsqueda y minería de información" de 4º del Grado en
 Ingeniería Informática, impartido en la Escuela Politécnica Superior de
 la Universidad Autónoma de Madrid. El fin del mismo, así como su uso,
 se ciñe a las actividades docentes de dicha asignatura.
"""

import whoosh
from whoosh.fields import Schema, TEXT, ID
from whoosh.formats import Format
from whoosh.qparser import QueryParser
from search import Searcher, tf, idf
from index import Index, Builder, TermFreq, DocVector
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os, os.path
import shutil
import zipfile
from statistics import term_stats
# A schema in Whoosh is the set of possible fields in a document in
# the search space. We just define a simple 'Document' schema
Document = Schema(
        path=ID(stored=True),
        content=TEXT(vector=Format)
    )

class WhooshBuilder(Builder):
    def __init__(self, directory):
        if os.path.exists(directory): shutil.rmtree(directory)
        os.makedirs(directory)
        self.writer = whoosh.index.create_in(directory, Document).writer()
    
    def build(self, collection):            
        if os.path.isfile(collection):
            if '.txt' in collection:
                fp = open(collection, 'r')
                urls = fp.readlines()
                for url in urls:
                    self.writer.add_document(path=url, content=BeautifulSoup(urlopen(url).read(), "html.parser").text)
                fp.close()
                return
            if '.zip' in collection:
                archive = zipfile.ZipFile(collection, 'r')
                for url in archive.namelist():
                    self.writer.add_document(path=url, content=BeautifulSoup(archive.read(url), "html.parser").text)
                archive.close()
                return
        files = os.listdir(collection)
        for doc in files:
            fp = open(collection + '/' + doc, "r")
            self.writer.add_document(path=doc, content=fp.read())
            fp.close()
        return

    def commit(self):
        self.writer.commit()

class WhooshIndex(Index):
    def __init__(self, path):            
        self.reader = whoosh.index.open_dir(path).reader()

        self.index_path = path
        
    # All terms returns only the term info. 
    def all_terms(self):
        info = []
        for i in self.reader.all_terms():
            if "\\x" not in str(i[1]):
                info.append(i[1].decode('ascii'))

        # Returning binary like in the given example
        return info
    
    # Concatenate the word with its frequency???
    def all_terms_with_freq(self):
        term_freq = []
        info = self.all_terms()

        for term in info:
            term_freq.append((term, self.reader.frequency("content", term)))
        
        return term_freq   

    # Frequency of a word in all documents
    def total_freq(self, term):
        return self.reader.frequency("content", term)

    # Frequency of a single word in a document 
    def term_freq(self, term, doc_id): 
        vector = self.reader.vector(doc_id, "content")
        vector.skip_to(term)
        if vector.id() == term:
            return vector.value_as("frequency")
        return 0

    # Returns the total number of documents that contain "term"
    def doc_freq(self, term):
        return self.reader.doc_frequency("content", term)

    # Returns path of document given by id = doc_id
    def doc_path(self, doc_id):
        return self.reader.stored_fields(doc_id)['path']

    # Given a document returns an array of the terms associated to their frequency 
    def doc_vector(self, doc_id):
        vector = []
        for i in self.reader.vector(doc_id, "content").items_as("frequency"):
            vector.append(TermFreq(i))
        return vector


    # Given a term matches every document with the frequncy of that term
    def postings(self, word):
        return self.reader.postings("content", word).items_as("frequency")
        
    def ndocs(self):
        return self.reader.doc_count_all()
    


class WhooshSearcher(Searcher):

    def __init__(self, path):
        self.index_path = path
        self.index = whoosh.index.open_dir(path)
        self.searcher = self.index.searcher()
        self.parser = QueryParser("content", schema=self.index.schema)
        term_stats(self.index, 'whooshSearcher.png')

    def search(self, query, cutoff):
        tuples = [] 
        for path, score in self.searcher.search(self.parser.parse(query)).items():
            tuples.append((self.index.reader().stored_fields(path)['path'], score))
        return tuples[:cutoff]


