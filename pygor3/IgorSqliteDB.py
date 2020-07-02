#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 11:02:28 2019

@author: alfaceor
"""

import sqlite3
import csv
from Bio import SeqIO
#import IgorAlignment_data
from .IgorSQL import *


###################
# TODO: Generalize to other kinds of database like postgres
###################

class IgorSqliteDB:
    """
    Class to create and load table or database with sequences
    """
    def __init__(self): #=None):
        # if flnIgorSQL is None:
        #     self.flnIgorSQL = "IgorDB.sql" # FIXME : VERY BAD WRAPP WITH INIT
        # else:
        #     self.flnIgorSQL = flnIgorSQL
        self.flnIgorSQL = "" # FIXME: this shouldn't be need it!

        self.flnIgorDB  = "" #flnIgorDB
        
        self.flnIgorIndexedSeq = ""
        self.flnIgorIndexedCDR3 = ""
        
        self.flnVGeneTemplate   = ""
        self.flnDGeneTemplate   = ""
        self.flnJGeneTemplate   = ""
        
        self.flnVAlignments     = ""
        self.flnDAlignments     = ""
        self.flnJAlignments     = ""
        
        self.flnVAnchors        = ""
        self.flnJAnchors        = ""

        self.flnIgorModel_Parms = ""
        self.flnIgorModel_Marginals = "" #

        self.flnIgorBestScenarios = ""
        
        self.conn               = None

        self.sql_cols_list = None
        self.sqlcmd_ins_bs = None
    
    #@classmethod
    def createSqliteDB(self, flnIgorDB):
        # FIXME: THIS METHOD SHOULD BE SOMETHING LIKE EXECUTE SQL SCRIPT and in particular
        """
        Create a SQLite database with the flnIgorDB sql script.
        """
        self.flnIgorDB = flnIgorDB
        self.conn = None
        try:
            self.conn = sqlite3.connect(flnIgorDB)
            qry = open(self.flnIgorSQL, 'r').read()
            cur = self.conn.cursor()
            cur.executescript(qry)
            self.conn.commit()
            cur.close()
            #self.conn.close()
        except sqlite3.Error as e:
            print(e)

    @classmethod
    def create_db(cls, flnIgorDB):
        """
        Connect (or create if not exits) with filename
        """
        cls = IgorSqliteDB()
        cls.flnIgorDB = flnIgorDB
        cls.connect_db()
        return cls

    def connect_db(self):
        """
        Connect (or create if not exits) to database
        """
        self.conn = sqlite3.connect(self.flnIgorDB)

    def executescript(self, cur, str_query):
        cur.executescript(str_query)

    def execute_query(self, str_query):
        """
        Execute sql script in the SQLite database .
        """
        try:
            self.conn = sqlite3.connect(self.flnIgorDB)
            cur = self.conn.cursor()
            cur.executescript(str_query)
            self.conn.commit()
            cur.close()
            # self.conn.close()
        except sqlite3.Error as e:
            print(e)

    def execute_select_query(self, str_query):
        """
        Execute sql script in the SQLite database .
        """
        try:
            self.conn = sqlite3.connect(self.flnIgorDB)
            cur = self.conn.cursor()
            cur.execute(str_query)
            #self.conn.commit()
            record = cur.fetchall()
            # print(record)
            # cur.close()
            return record
            #self.conn.close()
        except sqlite3.Error as e:
            print(e)

    def createSqliteDB_tmp(self):
        # TODO: create database in base of IgorSQL scripts
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.flnIgorDB)
            qry = sqlcmd_ct['indexed_sequences']
            cur = self.conn.cursor()
            cur.executescript(qry)
            self.conn.commit()
            cur.close()
            # self.conn.close()
        except sqlite3.Error as e:
            print(e)


    # TODO: load database by receiving a list of identifiers defined in IgorDictionaries
    def load_db(self, **kwargs):
        """
        Return a parameter
        """

        for key in kwargs.keys():
            # Create a database.
            print( sqlcmd_ct[key] )
            #print(key)
            self.insert_IgorIndexedSeq_FromCSVline()

            # cur = self.conn.cursor()
            # try:
            #     cur.execute('BEGIN TRANSACTION')
            #     with open(flnIgorIndexedSeq) as fp:
            #         csvline = fp.readline()
            #         while csvline:
            #             csvline = fp.readline()
            #             # print(csvline)
            #             self.insert_IgorIndexedSeq_FromCSVline(cur, csvline)
            #     cur.execute('COMMIT')
            #     # self.conn.commit()
            # except sqlite3.Error as e:
            #     print(e)

    def load_VDJ_Database(self, flnIgorIndexedSeq, flnVGeneTemplate, flnDGeneTemplate, flnJGeneTemplate, flnVAlignments, flnDAlignments, flnJAlignments):
        
        self.load_IgorIndexedSeq_FromCSV(flnIgorIndexedSeq )
        
        self.load_IgorGeneTemplate_FromFASTA("V",flnVGeneTemplate)
        self.load_IgorGeneTemplate_FromFASTA("D",flnDGeneTemplate)
        self.load_IgorGeneTemplate_FromFASTA("J",flnJGeneTemplate)
        
        self.load_IgorAlignments_FromCSV("V", flnVAlignments)
        self.load_IgorAlignments_FromCSV("D", flnDAlignments)
        self.load_IgorAlignments_FromCSV("J", flnJAlignments)
    
    ###############################################
    ####  IgorIndexedSeq Table Methods
    ###############################################
    def load_IgorIndexedSeq_FromCSV(self, flnIgorIndexedSeq):
        """
        Insert indexed sequence in database from csv igor indexed_seqs file.
        :param conn:
        :param csvline:
        :return:
        """
        self.execute_query(sqlcmd_ct['indexed_sequences'])
        self.flnIgorIndexedSeq = flnIgorIndexedSeq
        cur = self.conn.cursor()
        try:
            cur.execute('BEGIN TRANSACTION')
            with open(flnIgorIndexedSeq) as fp:
                csvline = fp.readline()
                while csvline:
                    csvline = fp.readline()
                    # print(csvline)
                    self.insert_IgorIndexedSeq_FromCSVline(cur, csvline)
            cur.execute('COMMIT')
            # self.conn.commit()
        except sqlite3.Error as e:
            print(e)


    def insert_IgorIndexedSeq_FromCSVline(self, cur, csvline):
        """
        Insert IGoR indexed_sequences on Database flnIgorDB
        :param csvline:
        """
        sql = ''' INSERT INTO IgorIndexedSeq(seq_index,sequence)
                  VALUES(?,?) '''
        
        csvline = csvline.replace('\n','')
        data = tuple(csvline.split(";"))
        if len(data) == 2:
            try:
                #cur = self.conn.cursor()
                cur.execute(sql, data)
                #self.conn.commit()
            except sqlite3.Error as e:
                print(data)
                print(e)
                pass

    def fetch_IgorIndexedSeq_By_seq_index(self, seq_index):
        """
        Fetch seq_index and sequence in Igor database.
        :param seq_index: string to specify the type of gene V, D or J
        :return: 
        """

        #print(gene_name)
        sqlSelect = "SELECT * FROM IgorIndexedSeq WHERE seq_index = "+str(seq_index)+";"
        #print(sqlSelect)
        cur = self.conn.cursor()
        cur.execute(sqlSelect)
        #if strGene == 'D':
        #    print(sqlSelect)
        record = cur.fetchone()
        return (record)

    def get_IgorIndexedSeq_By_seq_index(self, seq_index):
        record = self.fetch_IgorIndexedSeq_By_seq_index(seq_index)
        from .IgorIO import IgorIndexedSequence
        return IgorIndexedSequence.load_FromSQLRecord(record)

    def fetch_IgorIndexedSeq_By_seq_indexList(self, seq_indexList):
        """
        Fetch seq_index and sequence in Igor database.
        :param seq_index: string to specify the type of gene V, D or J
        :return: 
        """

        #print(gene_name)
        strSeq_indexList = str( tuple( sorted( set( seq_indexList ) ) )  )

        sqlSelect = "SELECT * FROM IgorIndexedSeq WHERE seq_index IN "+strSeq_indexList+";"
        #print(sqlSelect)
        cur = self.conn.cursor()
        cur.execute(sqlSelect)
        #if strGene == 'D':
        #    print(sqlSelect)
        record = cur.fetchall()
        return (record)


    ###############################################
    ####  IgorXGeneTemplate Tables Methods
    ###############################################
    def load_IgorGeneTemplate_FromFASTA(self, strGene, flnGeneTemplate):
        """
        Insert D Gene templates in database from fasta files used by IGoR.
        :param flnIgorGeneTemplate: Fasta file
        """
        # TODO: ADD A PANDAS OBJECT FOR RAPID ACCESS TO GENOMIC TEMPLATES.
        filename = {'V': self.flnVGeneTemplate, 'D' : self.flnDGeneTemplate, 'J': self.flnJGeneTemplate }
        filename[strGene] = flnGeneTemplate
        print(strGene, filename[strGene])
        # Create table if don't exits
        self.execute_query(sqlcmd_ct['genomic'+strGene + 's'])
        with open(filename[strGene], "r") as handle:
            for gene_id, bioRecord in enumerate(SeqIO.parse(handle, "fasta") ):
                self.insert_IgorGeneTemplate_FromBioRecord(strGene, gene_id, bioRecord)

    def insert_IgorGeneTemplate_FromBioRecord(self, strGene, gene_id, bioRecord):
        """
        Insert IGoR Gene template in Database flnIgorDB
        :param strGene: string to specify the type of gene V, D or J
        :param gene_id: id to identify the gene template
        :param bioRecord: Biopython record of the inserted sequence
        """
        sql = "INSERT INTO Igor"+strGene+"GeneTemplate("+strGene.lower()+"gene_id,gene_name,sequence) VALUES(?,?,?) "

        data = tuple([gene_id, str(bioRecord.description).strip(), str(bioRecord.seq)])
        try:
            cur = self.conn.cursor()
            cur.execute(sql, data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            pass

    def fetch_IgorGeneTemplate_By_gene_name(self, strGene, gene_name):
        """
        Fetch Gene templates in database from fasta files used by IGoR.
        :param strGene: string to specify the type of gene V, D or J
        :param flnIgorGeneTemplate: Fasta file
        """
        sqlSelect = "SELECT * FROM Igor"+strGene.upper()+"GeneTemplate WHERE gene_name =\""+gene_name+"\";"
        #print(sqlSelect)
        cur = self.conn.cursor()
        cur.execute(sqlSelect)
        #if strGene == 'D':
        #    print(sqlSelect)
        record = cur.fetchone()
        return (record)        
    
    def fetch_IgorGeneTemplate_By_gene_id(self, strGene, gene_id):
        """
        Fetch Gene templates in database from fasta files used by IGoR.
        :param strGene: string to specify the type of gene V, D or J
        :param gene_id: 
        """
        sqlSelect = "SELECT * FROM Igor"+strGene.upper()+"GeneTemplate WHERE "+strGene.lower()+"gene_id ="+str(gene_id)+";"
        cur = self.conn.cursor()
        cur.execute(sqlSelect)
        record = cur.fetchone()
        return (record)

    def load_IgorGeneAnchors_FromCSV(self, strGene, flnGeneAnchors):
        self.execute_query(sqlcmd_ct['gene'+strGene+'CDR3Anchors'])
        filename = {'V': self.flnVAnchors, 'J': self.flnJAnchors}
        filename[strGene] = flnGeneAnchors

        cur = self.conn.cursor()
        try:
            cur.execute('BEGIN TRANSACTION')
            with open(filename[strGene], "r") as fp:
                csvline = fp.readline()
                while csvline:
                    csvline = fp.readline()
                    # print(csvline)
                    self.insert_IgorIndexedSeq_FromCSVline(cur, csvline)
            cur.execute('COMMIT')
            # self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    # FIXME: TO COMPLETE
    def insert_IgorGeneAnchors_FromCSVline(self, cur, csvline):
        """
        Insert IGoR indexed_CDR3_sequences in Database flnIgorDB
        :param csvline:
        """
        sql = ''' INSERT INTO IgorIndexedSeq(seq_index,sequence)
                  VALUES(?,?) '''

        csvline = csvline.replace('\n', '')
        data = tuple(csvline.split(";"))
        if len(data) == 2:
            try:
                # cur = self.conn.cursor()
                cur.execute(sql, data)
                # self.conn.commit()
            except sqlite3.Error as e:
                print(data)
                print(e)
                pass

    ###############################################
    ####  IgorXAlignments Tables Methods
    ###############################################
    
    def load_IgorAlignments_FromCSV(self, strGene, flnAlignments):
        """
        Insert Gene templates in database from fasta files used by IGoR.
        :param strGene: string to specify the type of gene V, D or J
        :param flnIgorGeneTemplate: Fasta file
        """

        # Load database from file
        strGene = strGene.upper()
        filename = {'V': self.flnVAlignments, 'D' : self.flnDAlignments, 'J': self.flnJAlignments}
        filename[strGene] = flnAlignments
        # Create table if don't exits
        self.execute_query(sqlcmd_ct[strGene + '_alignments'])
        try:
            cur = self.conn.cursor()
            cur.execute('BEGIN TRANSACTION')
            with open(filename[strGene]) as fp:
                csvline = fp.readline()
                while csvline:
                    csvline = fp.readline()
                    #print(csvline)
                    self.insert_IgorAlignments_FromCSVline(cur, strGene, csvline)
            
            cur.execute('COMMIT')
        except sqlite3.Error as e:
            print(e)

    def insert_IgorAlignments_FromCSVline(self, cur, strGene, csvline):
        """
        Insert IGoR Alignments on Database flnIgorDB
        :param strGene: string to specify the type of gene V, D or J
        :param csvline:
        """
        sqlBase = '''INSERT INTO Igor{}Alignments(
                seq_index, 
                {}gene_id, 
                score,
                offset,
                insertions,
                deletions,
                mismatches,
                length,
                offset_5_p_align,
                offset_3_p_align) 
                VALUES(?,?,?,?,?,?,?,?,?,?)
                '''
        
        strGene =  strGene.upper()
        sql = sqlBase.format(strGene.upper(), strGene.lower())
        # search on IgorGeneTemplate the corresponding Gene id 
        csvline = csvline.replace("{","[").replace("}","]").replace('\n','')
        csvlist = csvline.split(";")
        if len(csvlist) == 10 :
            gene_name = csvlist[1]
            gene_name = gene_name.strip()
            gene_id = self.fetch_IgorGeneTemplate_By_gene_name(strGene, gene_name)[0]
            #print(gene_id, gene_name)
            csvlist[1] = str(gene_id)
            data = tuple(csvlist)
            #print(data)
            try:
                #cur = self.conn.cursor()
                cur.execute(sql, data)
                #self.conn.commit()
            except sqlite3.Error as e:
                print(e)
                pass
        else:
            print(csvlist)

    def fetch_IgorAlignments_By_seq_index(self, strGene, seq_index, limit=None):
        """
        Fetch IgorAlignments from database by seq_index.
        :param strGene: string to specify the type of gene V, D or J
        :param seq_index: IgorIndexedSequences index
        """
        sqlSelect = "SELECT * FROM Igor"+strGene.upper()+"Alignments WHERE seq_index=="+str(seq_index)+" ORDER BY score DESC"
        if limit is not None:
            sqlSelect = sqlSelect + " LIMIT "+ str(limit)
        cur = self.conn.cursor()
        cur.execute(sqlSelect)
        record = cur.fetchall()
        return (record)

    def fetch_best_IgorAlignments_By_seq_index(self, strGene, seq_index):
        """
        Fetch IgorAlignments from database by seq_index.
        :param strGene: string to specify the type of gene V, D or J
        :param seq_index: IgorIndexedSequences index
        """
        sqlSelect = "SELECT * FROM Igor" + strGene.upper() + "Alignments WHERE seq_index==" + str(
            seq_index) + " ORDER BY score DESC LIMIT 1"
        cur = self.conn.cursor()
        cur.execute(sqlSelect)
        record = cur.fetchone()
        return (record)

    def get_best_IgorAlignment_data_By_seq_index(self, strGene, seq_index):
        from .IgorIO import IgorAlignment_data
        best_align_data_record = self.fetch_best_IgorAlignments_By_seq_index(strGene, seq_index)
        # print("best_align_data_record ", best_align_data_record)
        best_align_data = IgorAlignment_data.load_FromSQLRecord(best_align_data_record)
        best_align_data.strGene_class = strGene

        gene_record = self.fetch_IgorGeneTemplate_By_gene_id(best_align_data.strGene_class, best_align_data.gene_id)
        best_align_data.strGene_name = gene_record[1]
        best_align_data.strGene_seq = gene_record[2]
        return best_align_data

    # TODO: Create an IgorAlignment_data instance with a better sql query (join the necessary tables.)
    # TODO:
    def get_IgorAlignment_data_list_query(self, strGene, seq_index, where=None):
        sqlSelect = "SELECT * FROM Igor" + strGene.upper() + "Alignments WHERE seq_index==" + str(seq_index) + ""
        from .IgorIO import IgorAlignment_data
        align_data_records = self.fetch_IgorAlignments_By_seq_index(strGene, seq_index)
        align_data_list = list()
        for align_record in align_data_records:
            align_data = IgorAlignment_data.load_FromSQLRecord(align_record)
            align_data.strGene_class = strGene

            gene_record = self.fetch_IgorGeneTemplate_By_gene_id(align_data.strGene_class, align_data.gene_id)
            align_data.strGene_name = gene_record[1]
            align_data.strGene_seq = gene_record[2]
            align_data_list.append(align_data)
        return align_data_list

    def get_IgorAlignment_data_list_By_seq_index(self, strGene, seq_index, limit=None):
        from .IgorIO import IgorAlignment_data
        align_data_records = self.fetch_IgorAlignments_By_seq_index(strGene, seq_index, limit=limit)
        # best_align_data_record = self.fetch_best_IgorAlignments_By_seq_index(strGene, seq_index)
        #print("best_align_data_record ", align_data_records)
        align_data_list = list()
        for align_record in align_data_records:
            align_data = IgorAlignment_data.load_FromSQLRecord(align_record)
            align_data.strGene_class = strGene

            gene_record = self.fetch_IgorGeneTemplate_By_gene_id(align_data.strGene_class, align_data.gene_id)
            align_data.strGene_name = gene_record[1]
            align_data.strGene_seq = gene_record[2]
            align_data_list.append(align_data)
        return align_data_list

    def appendList_IgorAlignments_data_By_seq_index(self, strGene_class, seq_index, alnDataList=None):
        """
        Append to a list of IgorAlignment_data objects given gene class ("V", "D", "J"), seq_index 
        append a list to append the objects.
        :param strGene_class: string to specify the type of gene V, D or J.
        :param seq_index: IgorIndexedSequences index.
        :param alnDataList: List of IgorAlignment_data objects.
        """
        if alnDataList == None:
            alnDataList = list()
        
        try:
            alignsSQLrecords = self.fetch_IgorAlignments_By_seq_index(strGene_class, seq_index)
            for alignSQLrecord in alignsSQLrecords:
                #print(alignSQLrecord)
                gene_id = alignSQLrecord[1]
                geneTemplateRecord = self.fetch_IgorGeneTemplate_By_gene_id(strGene_class, gene_id)
                strGene_name = geneTemplateRecord[1]
                strGene_seq  = geneTemplateRecord[2]
                aln_data = IgorAlignment_data.IgorAlignment_data.load_FromSQLRecord(alignSQLrecord, strGene_name=strGene_name)
                aln_data.strGene_class = strGene_class
                aln_data.strGene_seq   = strGene_seq
                alnDataList.append(aln_data)
                #print(aln_data.strGene_name, aln_data.score, aln_data.offset, aln_data.insertions)
            return alnDataList
        except Exception as e:
            print(e)
    
    def write_IgorAlignments2Fasta(self, alnDataList):
        print(alnDataList)

    def get_naive_sequence_from_IgorAligment_data(self, seq_index):
        # TODO: use self.dicts and IgorAlignment_data to reconstruct sequence
        # 1. get Indexed Sequence
        indexed_sequence = self.get_IgorIndexedSeq_By_seq_index(seq_index)
        indexed_sequence.offset = 0
        # 2. get Alignments

        # 3. Choose best V and J alignment
        best_v_align_data = self.get_best_IgorAlignment_data_By_seq_index('V', indexed_sequence.seq_index)
        best_j_align_data = self.get_best_IgorAlignment_data_By_seq_index('J', indexed_sequence.seq_index)

        # 4. if D exists then choose the best D gene where offsets are between CDR3 anchors
        d_align_data_list = self.get_IgorAlignment_data_list_By_seq_index('D', indexed_sequence.seq_index)

        # 5. Once D select the highest score.
        # 6. if there is an overlap in V or J segments then, removing that segment

        return ""

    # def get_naive_alignment(self, seq_index):
    #     alnDataListV = db.fetch_IgorAlignments_By_seq_index('V', seq_index)
    #     v_align_data = p3.IgorAlignment_data.load_FromSQLRecord(alnDataListV[0])
    #     print(v_align_data.to_dict())
    #     v_gene_seq = db.fetch_IgorGeneTemplate_By_gene_id('V', v_align_data.gene_id)[2]
    #     print(v_gene_seq)

    def load_IgorIndexedCDR3_FromCSV(self, flnIgorIndexedCDR3):
        """
                Insert indexed CDR3 in database from csv igor indexed_seqs file.
                :param conn:
                :param csvline:
                :return:
                """
        self.execute_query(sqlcmd_ct['indexed_CDR3'])

        self.flnIgorIndexedCDR3 = flnIgorIndexedCDR3
        cur = self.conn.cursor()
        try:
            cur.execute('BEGIN TRANSACTION')
            with open(self.flnIgorIndexedCDR3) as fp:
                csvline = fp.readline()
                while csvline:
                    csvline = fp.readline()
                    # print(csvline)
                    self.insert_IgorIndexedCDR3_FromCSVline(cur, csvline)
            cur.execute('COMMIT')
            # self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def insert_IgorIndexedCDR3_FromCSVline(self, cur, csvline):
        """
        Insert IGoR indexed_sequences on Database flnIgorDB
        :param csvline:
        """
        # seq_index;v_anchor;j_anchor;CDR3nt;CDR3aa
        sql = ''' INSERT INTO IgorIndexedCDR3(seq_index,v_anchor,j_anchor,CDR3,CDR3_aa)
                  VALUES(?,?,?,?,?) '''

        csvline = csvline.replace('\n', '')
        # FIXME: CHANGE THIS ONLY SAVE THE ANCHORS AND NOT THE CDR3 and CDR3_aa
        # data = tuple(csvline.split(";")[0:2]) # to pick just seq_index, v_anchor, j_anchor
        # if len(data) == 2:
        data = tuple(csvline.split(";"))
        # if len(data) == 2:
        try:
            # cur = self.conn.cursor()
            cur.execute(sql, data)
            # self.conn.commit()
        except sqlite3.Error as e:
            print(data)
            print(e)
            pass

    def fetch_IgorIndexedCDR3_By_seq_index(self, seq_index):
        # print(gene_name)
        sqlSelect = "SELECT * FROM IgorIndexedCDR3 WHERE seq_index = " + str(seq_index) + ";"
        # print(sqlSelect)
        cur = self.conn.cursor()
        cur.execute(sqlSelect)
        # if strGene == 'D':
        #    print(sqlSelect)
        record = cur.fetchone()
        return (record)

    # def get_IgorIndexedCDR3_By_seq_index(self, seq_index):
    #     record = self.fetch_IgorIndexedCDR3_By_seq_index(seq_index)
    #     return IgorIndexedSequence.load_FromSQLRecord(record)

    ############################
    def load_IgorModel_Parms(self, mdl_parms): #fln_model_parms):
        ################## TODO: Insert Event_list
        self.execute_query(sqlcmd_ct['MP_Event_list'])
        # self.flnIgorModel_Parms = fln_model_parms
        cur = self.conn.cursor()
        try:
            cur.execute('BEGIN TRANSACTION')

            from .IgorIO import IgorModel_Parms
            # mdl_parms = IgorModel_Parms(model_parms_file=fln_model_parms)

            for event in mdl_parms.Event_list:
                event_dict = event.to_dict()
                # print("-"*50, event.nickname)
                event_realizations_list = event_dict.pop('realizations')
                event_dict['realizations_table'] = "IgorER_" + event_dict['nickname']
                self.insert_IgorRec_Event_FromDict(cur, event_dict)
                # Create database with realizations
                script_table = sqlcmd_ct['ER_event_template'].format(event_dict['realizations_table'])
                # insert realizations from realizations object
                try:
                    # Create table of realizations
                    cur.execute(script_table)
                    # Insert realizations
                    for realization in event_realizations_list:
                        # print(realization.to_dict())
                        self.insert_IgorEvent_realization_FromDict(cur, event_dict['realizations_table'], realization.to_dict())
                except sqlite3.Error as e:
                    print(e)

            cur.execute('COMMIT')
            # self.conn.commit()
        except sqlite3.Error as e:
            print("Can't create IgorModel_Parms table")
            print(e)

        ################## TODO: Insert Edges XXX
        # Create database if not exist.
        self.execute_query(sqlcmd_ct['MP_Edges'])
        cur = self.conn.cursor()
        sql = 'INSERT INTO IgorMP_Edges(parent_event,child_event) VALUES (?,?)'
        cur.execute('BEGIN TRANSACTION')
        for edge in mdl_parms.Edges:
            # Insert in Edges table
            try:
                # cur = self.conn.cursor()
                data = (mdl_parms.dictNameNickname[ edge[0] ], mdl_parms.dictNameNickname[ edge[1] ])
                print(data)
                cur.execute(sql, data)
                # self.conn.commit()
            except sqlite3.Error as e:
                print(edge, data)
                print(e)
                exit()
                # pass
        cur.execute('COMMIT')

        ################## TODO: Insert ErrorRate
        self.execute_query(sqlcmd_ct['MP_ErrorRate'])
        cur = self.conn.cursor()
        columns = ', '.join(mdl_parms.ErrorRate_dict.keys())
        placeholders = ':' + ', :'.join(mdl_parms.ErrorRate_dict.keys())
        sql = 'INSERT INTO IgorMP_ErrorRate (%s) VALUES (%s)' % (columns, placeholders)
        cur.execute('BEGIN TRANSACTION')
        print(mdl_parms.ErrorRate_dict)
        cur.execute(sql, mdl_parms.ErrorRate_dict)
        cur.execute('COMMIT')

    def insert_IgorRec_Event_FromDict(self, cur, event_dict: dict):
        # print(event_dict.keys())
        columns = ', '.join(event_dict.keys())
        placeholders = ':' + ', :'.join(event_dict.keys())
        sql = 'INSERT INTO IgorMP_Event_list (%s) VALUES (%s)' % (columns, placeholders)
        # print(sql)
        try:
            # cur = self.conn.cursor()
            cur.execute(sql, event_dict)
            # self.conn.commit()
        except sqlite3.Error as e:
            print(event_dict)
            print(e)
            pass

    def insert_IgorEvent_realization_FromDict(self, cur, event_table, event_realization_dict):
        # TODO: IgorEvent_realization
        columns = ', '.join(event_realization_dict.keys())
        placeholders = ':' + ', :'.join(event_realization_dict.keys())
        tmp_sql = 'INSERT INTO '+event_table+' (%s) VALUES (%s)'
        sql = tmp_sql % (columns, placeholders)
        # print(sql)
        try:
            # cur = self.conn.cursor()
            cur.execute(sql, event_realization_dict)
            # self.conn.commit()
        except sqlite3.Error as e:
            print(event_realization_dict)
            print(e)
            pass

    def load_IgorModel_Marginals(self, mdl_xdata:dict):
        for event_nickname in mdl_xdata.keys():
            da = mdl_xdata[event_nickname]
            lista = list(dict(da.coords).keys())
            # print(lista)
            for dim in da.dims:
                lista.remove(dim)
            da = da.drop(lista)
            # Create table of not real marginals
            # TODO: CONTINUE create tables
            if da.attrs['event_type'] == 'DinucMarkov':
                # TODO: ADD X AND Y WITH THE CORRESPONDING IDS
                self.execute_query( sqlcmd_ct_Model_Marginals_DinucMarkov(event_nickname, ['x', 'y']) )
            else:
                tmp_list = [event_nickname] + da.attrs['parents']
                da = da.transpose(*tmp_list)
                # Create table for model marginals
                self.execute_query( sqlcmd_ct_Model_Marginals(event_nickname, da.attrs['parents']) )

                cur = self.conn.cursor()
                try:
                    cur.execute('BEGIN TRANSACTION')
                    df = da.to_dataframe(name='P')
                    df.reset_index(inplace=True)

                    # Rename names of dataframe
                    dicto2rename = dict()
                    for col in df.columns:
                        print(col)
                        if not col == 'P':
                            dicto2rename[col] = "id_"+col
                    df.rename(dicto2rename, axis='columns', inplace=True)

                    mm_table = "IgorMM_"+event_nickname
                    columns_list = list(df.columns)
                    str_columns = ",".join(columns_list )
                    placeholders = ':' + ', :'.join(columns_list)
                    sql = 'INSERT INTO ' + mm_table + ' (%s) VALUES (%s)' % (str_columns, placeholders)

                    for index, row in df.iterrows():
                        dicto = row.to_dict()
                        cur.execute(sql, row.to_dict())
                    cur.execute('COMMIT')
                    # self.conn.commit()
                except sqlite3.Error as e:
                    print("Can't insert in "+event_nickname+" table")
                    print(e)

    def insert_IgorModel_Marginals_FromDict(self, cur, event_table, event_realization_dict):
        # TODO: IgorEvent_realization
        columns = ', '.join(event_realization_dict.keys())
        placeholders = ':' + ', :'.join(event_realization_dict.keys())
        tmp_sql = 'INSERT INTO '+event_table+' (%s) VALUES (%s)'
        sql = tmp_sql % (columns, placeholders)
        # print(sql)
        try:
            # cur = self.conn.cursor()
            cur.execute(sql, event_realization_dict)
            # self.conn.commit()
        except sqlite3.Error as e:
            print(event_realization_dict)
            print(e)
            pass

    def load_IgorModel_FromTXT(self, flnIgorModel_Parms, flnIgorModel_Marginals):
        self.flnIgorModel_Parms = flnIgorModel_Parms
        self.flnIgorModel_Marginals = flnIgorModel_Marginals
        from .IgorIO import IgorModel
        mdl = IgorModel(model_parms_file=flnIgorModel_Parms, model_marginals_file=flnIgorModel_Marginals)
        self.load_IgorModel(self, mdl)

    def load_IgorModel(self, mdl):
        self.load_IgorModel_Parms(mdl.parms)
        self.load_IgorModel_Marginals(mdl.xdata)

    def load_IgorBestScenarios_FromCSV(self, flnIgorBestScenarios, mdl):
        self.flnIgorBestScenarios = flnIgorBestScenarios
        with open(self.flnIgorBestScenarios, "r") as fp:
            #### CREATE DATABASE
            ## Get best scenarios header file
            igor_bsfileHeader = fp.readline().replace('\n', '').replace('Mismatches', 'mismatches')
            file_header_list = igor_bsfileHeader.split(';')
            bs_events_name_list = file_header_list[3:-1]
            ## Change event_name to event_nickname using dictionary.
            # Get dictionary to change names to nicknames
            events_name_nickname_dict = mdl.parms.get_event_dict('name', 'nickname')
            bs_events_nickname_list = [ events_name_nickname_dict[event_name] for event_name in bs_events_name_list]

            # Now generate sql_id, sql_type and foreign_key in the file order
            events_dict_list = list()
            sql_list_ct_table_cols = list()
            sql_list_ct_table_foreign_keys = list()
            sql_list_ins_table = list()
            self.sql_list_of_listtypes = list()
            for ii, event_nickname in enumerate(bs_events_nickname_list) :
                event = mdl.parms.get_Event(event_nickname)
                event_dict = event.to_dict()
                del event_dict['realizations']
                if event.event_type == 'DinucMarkov':
                    event_dict['sql_id'] = event.nickname
                    event_dict['sql_type'] = "text"
                    sql_list_ct_table_cols.append(event_dict['sql_id']+" "+event_dict['sql_type'])
                    sql_list_ins_table.append(event_dict['sql_id'])
                    self.sql_list_of_listtypes.append(3+ii)
                else:
                    event_dict['sql_id'] = 'id_'+event.nickname
                    event_dict['sql_type'] = "integer"
                    event_dict['sql_foreign_key'] = "FOREIGN KEY (id_{}) REFERENCES IgorER_{} (id)".format(event_nickname, event_nickname)
                    sql_list_ct_table_cols.append(event_dict['sql_id'] + " " + event_dict['sql_type'])
                    sql_list_ins_table.append(event_dict['sql_id'])
                    sql_list_ct_table_foreign_keys.append(event_dict['sql_foreign_key'])
                events_dict_list.append(event_dict)

            self.sql_list_of_listtypes.append(3+len(bs_events_nickname_list)) # mismatches position

            # Now make script to create table in database and create table
            self.execute_query(
                sqlcmd_ct['BestScenario_template'].format(','.join(sql_list_ct_table_cols),
                                                          ','.join(sql_list_ct_table_foreign_keys))
            )

            ### INSERT VALUES
            sql_cols_list =['seq_index', 'scenario_rank', 'scenario_proba_cond_seq'] + sql_list_ins_table + ['mismatches', 'mismatcheslen']
            sql_str_cols = ','.join(sql_cols_list)
            sql_str_aux = ','.join(['?' for col in sql_cols_list])

            self.sql_cols_list = sql_cols_list
            self.sqlcmd_ins_bs = ''' INSERT INTO IgorBestScenarios({}) VALUES({}) '''.format(sql_str_cols, sql_str_aux)

            #print(self.sqlcmd_ins_bs)

            # INSERT VALUES IN DATABASE
            cur = self.conn.cursor()
            try:
                cur.execute('BEGIN TRANSACTION')
                with open(self.flnIgorBestScenarios) as fp:
                    csvline = fp.readline()
                    while csvline:
                        csvline = fp.readline()
                        self.insert_IgorBestScenarios_FromCSVline(cur, csvline)
                cur.execute('COMMIT')
                # self.conn.commit()
            except sqlite3.Error as e:
                print(e)


    def insert_IgorBestScenarios_FromCSVline(self, cur, csvline):
        # sql = ''' INSERT INTO IgorBestScenarios({}) VALUES({}) '''
        csvline = csvline.replace('\n', '')
        csvlist = csvline.split(";")
        # FIXME: FIND A BETTER WAY TO REPLACE THE TYPE FOR INSERTION
        for ii in range(len(csvlist)):
            if ii in self.sql_list_of_listtypes:
                csvlist[ii] = csvlist[ii].replace("(", "[").replace(")", "]")  # lists vd_dinucl, dj_dinucl, mismatches
            else:
                csvlist[ii] = csvlist[ii].replace("(", "").replace(")", "")

        # print(csvlist)

        # data[-1] convert it to list and
        try:
            data = csvlist + [len(eval(csvlist[-1]))]
            try:
                # cur = self.conn.cursor()
                cur.execute(self.sqlcmd_ins_bs, data)
                # self.conn.commit()
            except sqlite3.Error as e:
                print(data)
                print(e)
                pass
        except Exception as e:
            print("ohohohoho")
            print(csvlist)
            print(e)
            pass






