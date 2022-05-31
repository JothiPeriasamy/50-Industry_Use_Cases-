from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, RDFS, XSD
import csv
import spotlight

class Knowledge_Base:
    def __init__(self):
        self.vAR_ex = Namespace("http://example.org/")
        self.exdata = Namespace("http://example.org/data#")

        self.vAR_g = Graph()

    def define_relations(self):
        self.vAR_g.add( (self.vAR_ex.Organization, RDF.type, RDFS.Class) )
        self.vAR_g.add( (self.vAR_ex.Organization, RDFS.subClassOf, FOAF.Organization) )
        self.vAR_g.add( (self.vAR_ex.Organization, RDFS.label, Literal("Organization", lang="en")) )
        self.vAR_g.add( (self.vAR_ex.Organization, RDFS.comment, Literal("Organization at which the students enroll")) )

        self.vAR_g.add( (self.vAR_ex.Use_case, RDF.type, RDFS.Class) )
        self.vAR_g.add( (self.vAR_ex.Use_case, RDFS.label, Literal("Use_case", lang="en")) )
        self.vAR_g.add( (self.vAR_ex.Use_case, RDFS.comment, Literal("Use-cases are offered at an organisation to enhance students ability towards working on industrial problems")) )
        self.vAR_g.add( (self.vAR_ex.Use_case, FOAF.name, XSD.string) )
        self.vAR_g.add( (self.vAR_ex.Use_case, self.vAR_ex.hasSubject, XSD.string) )
        self.vAR_g.add( (self.vAR_ex.Use_case, self.vAR_ex.hasNumber, XSD.integer) )
        self.vAR_g.add( (self.vAR_ex.Use_case, self.vAR_ex.hasDescription, XSD.string) )

        self.vAR_g.add( (self.vAR_ex.Student, RDF.type, RDFS.Class) )
        self.vAR_g.add( (self.vAR_ex.Student, RDFS.subClassOf, FOAF.Person) )
        self.vAR_g.add( (self.vAR_ex.Student, RDFS.label, Literal("Student", lang="en")) )
        self.vAR_g.add( (self.vAR_ex.Student, RDFS.comment, Literal("Person who enrolls at a Organization_data")) )
        self.vAR_g.add( (self.vAR_ex.Student, FOAF.name, XSD.string) )
        self.vAR_g.add( (self.vAR_ex.Student, self.vAR_ex.hasID, XSD.integer) )
        self.vAR_g.add( (self.vAR_ex.Student, FOAF.mbox, XSD.string) )
        self.vAR_g.add( (self.vAR_ex.Student, self.vAR_ex.hasEnrolled, self.vAR_ex.Use_case) )

        self.vAR_g.add( (self.vAR_ex.hasSubject, RDF.type, RDF.Property) )
        self.vAR_g.add( (self.vAR_ex.hasSubject, RDFS.label, Literal("hasSubject", lang="en")) )
        self.vAR_g.add( (self.vAR_ex.hasSubject, RDFS.comment, Literal("Use_case has a subject")) )
        self.vAR_g.add( (self.vAR_ex.hasSubject, RDFS.domain, self.vAR_ex.Use_case) )
        self.vAR_g.add( (self.vAR_ex.hasSubject, RDFS.range, XSD.string) )

        self.vAR_g.add( (self.vAR_ex.hasNumber, RDF.type, RDF.Property) )
        self.vAR_g.add( (self.vAR_ex.hasNumber, RDFS.label, Literal("hasNumber", lang="en")) )
        self.vAR_g.add( (self.vAR_ex.hasNumber, RDFS.comment, Literal("Use_case has a number")) )
        self.vAR_g.add( (self.vAR_ex.hasNumber, RDFS.domain, self.vAR_ex.Use_case) )
        self.vAR_g.add( (self.vAR_ex.hasNumber, RDFS.range, XSD.integer) )

        self.vAR_g.add( (self.vAR_ex.hasID, RDF.type, RDF.Property) )
        self.vAR_g.add( (self.vAR_ex.hasID, RDFS.label, Literal("hasID", lang="en")) )
        self.vAR_g.add( (self.vAR_ex.hasID, RDFS.comment, Literal("Student has an ID number")) )
        self.vAR_g.add( (self.vAR_ex.hasID, RDFS.domain, self.vAR_ex.Student) )
        self.vAR_g.add( (self.vAR_ex.hasID, RDFS.range, XSD.integer) )

        self.vAR_g.add( (self.vAR_ex.hasEnrolled, RDF.type, RDF.Property) )
        self.vAR_g.add( (self.vAR_ex.hasEnrolled, RDFS.label, Literal("hasEnrolled", lang="en")) )
        self.vAR_g.add( (self.vAR_ex.hasEnrolled, RDFS.comment, Literal("Student has Enrolled in a Use_case")) )
        self.vAR_g.add( (self.vAR_ex.hasEnrolled, RDFS.domain, self.vAR_ex.Student) )
        self.vAR_g.add( (self.vAR_ex.hasEnrolled, RDFS.range, self.vAR_ex.Use_case) )

    def add_data(self):
        with open("D:\\ConvAI\\DSAI_Organization_Data_1") as data:
            file = csv.reader(data, delimiter=',')
            for row in file:
                Organization = URIRef(self.exdata + row[0].replace(" ", "_")) 
                link = URIRef(row[1]) 

                self.vAR_g.add( (Organization, RDF.type, self.vAR_ex.Organization) )
                self.vAR_g.add( (Organization, FOAF.name, Literal(row[0])) )
                self.vAR_g.add( (Organization, RDFS.seeAlso, link) )

        with open("D:\\ConvAI\\DSAI_Use-case_Data_1") as data:
            file = csv.reader(data, delimiter=',')
            for row in file:
                Use_case = URIRef(self.exdata + row[0].replace(" ", "_")) 
                link = URIRef(row[3]) 
                
                self.vAR_g.add( (Use_case, RDF.type, self.vAR_ex.Use_case) )
                self.vAR_g.add( (Use_case, FOAF.name, Literal(row[0])) )
                self.vAR_g.add( (Use_case, self.vAR_ex.hasSubject, Literal(row[1])) )
                self.vAR_g.add( (Use_case, self.vAR_ex.hasNumber, Literal(row[2])) )
                self.vAR_g.add( (Use_case, RDFS.seeAlso, link) )

        with open("D:\\ConvAI\\DSAI_Student_Data_1") as data:
            file = csv.reader(data, delimiter=',')
            for row in file:
                student = URIRef(self.exdata + row[0].replace(" ", "_")) 
                Use_case = URIRef(self.exdata + row[3].replace(" ", "_")) 

                for s, p, o in self.vAR_g:
                    if not (student, RDF.type, self.vAR_ex.Student) in self.vAR_g:
                        self.vAR_g.add( (student, RDF.type, self.vAR_ex.Student) )
                        self.vAR_g.add( (student, FOAF.name, Literal(row[0])) )
                        self.vAR_g.add( (student, self.vAR_ex.hasID, Literal(row[1])) )
                        self.vAR_g.add( (student, FOAF.mbox, Literal(row[2])) )

                        if not (row[3] == ''):
                            self.vAR_g.add( (student, self.vAR_ex.hasEnrolled, Use_case) )
                    else:
                        if not (row[3] == ''):
                            self.vAR_g.add( (student, self.vAR_ex.hasEnrolled, Use_case) )

    def push_data(self):
        # print graph in N-Triples format to knowledge_base.nt file
        # run this only once to populate the .nt file
        # ttl[better clarity]/nt
        print(self.vAR_g.serialize("D:\\ConvAI\\DSAI_Knowledge_Base_1.nt", format="nt"))

    def run_all(self):
        self.define_relations()
        self.add_data()
        self.push_data()

vAR_obj = Knowledge_Base()
vAR_obj.run_all()