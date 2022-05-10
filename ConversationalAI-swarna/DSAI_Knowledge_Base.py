from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, RDFS, XSD
import csv
import spotlight

# define namespaces
vAR_ex = Namespace("http://example.org/")
exdata = Namespace("http://example.org/data#")

vAR_g = Graph()

# create knowledge base
vAR_g.add( (vAR_ex.University, RDF.type, RDFS.Class) )
vAR_g.add( (vAR_ex.University, RDFS.subClassOf, FOAF.Organization) )
vAR_g.add( (vAR_ex.University, RDFS.label, Literal("University", lang="en")) )
vAR_g.add( (vAR_ex.University, RDFS.comment, Literal("Organization at which the students go to")) )

vAR_g.add( (vAR_ex.Course, RDF.type, RDFS.Class) )
vAR_g.add( (vAR_ex.Course, RDFS.label, Literal("Course", lang="en")) )
vAR_g.add( (vAR_ex.Course, RDFS.comment, Literal("Course is offered at a university_data towards the granting of an approved degree")) )
vAR_g.add( (vAR_ex.Course, FOAF.name, XSD.string) )
vAR_g.add( (vAR_ex.Course, vAR_ex.hasSubject, XSD.string) )
vAR_g.add( (vAR_ex.Course, vAR_ex.hasNumber, XSD.integer) )
vAR_g.add( (vAR_ex.Course, vAR_ex.hasDescription, XSD.string) )
vAR_g.add( (vAR_ex.Course, RDFS.seeAlso, XSD.anyURI) )
vAR_g.add( (vAR_ex.Course, vAR_ex.hasTopic, vAR_ex.Topic) )

vAR_g.add( (vAR_ex.Topic, RDF.type, RDFS.Class) )
vAR_g.add( (vAR_ex.Topic, RDFS.label, Literal("Topic", lang="en")) )
vAR_g.add( (vAR_ex.Topic, RDFS.comment, Literal("Topic is part of a course material")) )
vAR_g.add( (vAR_ex.Topic, FOAF.name, XSD.string) )
vAR_g.add( (vAR_ex.Topic, RDFS.seeAlso, XSD.anyURI) )

vAR_g.add( (vAR_ex.Student, RDF.type, RDFS.Class) )
vAR_g.add( (vAR_ex.Student, RDFS.subClassOf, FOAF.Person) )
vAR_g.add( (vAR_ex.Student, RDFS.label, Literal("Student", lang="en")) )
vAR_g.add( (vAR_ex.Student, RDFS.comment, Literal("Person who studies at a university_data")) )
vAR_g.add( (vAR_ex.Student, FOAF.name, XSD.string) )
vAR_g.add( (vAR_ex.Student, vAR_ex.hasID, XSD.integer) )
vAR_g.add( (vAR_ex.Student, FOAF.mbox, XSD.string) )
vAR_g.add( (vAR_ex.Student, vAR_ex.hasCompleted, vAR_ex.Course) )

vAR_g.add( (vAR_ex.hasSubject, RDF.type, RDF.Property) )
vAR_g.add( (vAR_ex.hasSubject, RDFS.label, Literal("hasSubject", lang="en")) )
vAR_g.add( (vAR_ex.hasSubject, RDFS.comment, Literal("Course has a subject")) )
vAR_g.add( (vAR_ex.hasSubject, RDFS.domain, vAR_ex.Course) )
vAR_g.add( (vAR_ex.hasSubject, RDFS.range, XSD.string) )

vAR_g.add( (vAR_ex.hasNumber, RDF.type, RDF.Property) )
vAR_g.add( (vAR_ex.hasNumber, RDFS.label, Literal("hasNumber", lang="en")) )
vAR_g.add( (vAR_ex.hasNumber, RDFS.comment, Literal("Course has a number")) )
vAR_g.add( (vAR_ex.hasNumber, RDFS.domain, vAR_ex.Course) )
vAR_g.add( (vAR_ex.hasNumber, RDFS.range, XSD.integer) )

vAR_g.add( (vAR_ex.hasDescription, RDF.type, RDF.Property) )
vAR_g.add( (vAR_ex.hasDescription, RDFS.label, Literal("hasDescription", lang="en")) )
vAR_g.add( (vAR_ex.hasDescription, RDFS.comment, Literal("Course has a description")) )
vAR_g.add( (vAR_ex.hasDescription, RDFS.domain, vAR_ex.Course) )
vAR_g.add( (vAR_ex.hasDescription, RDFS.range, XSD.string) )

vAR_g.add( (vAR_ex.hasID, RDF.type, RDF.Property) )
vAR_g.add( (vAR_ex.hasID, RDFS.label, Literal("hasID", lang="en")) )
vAR_g.add( (vAR_ex.hasID, RDFS.comment, Literal("Student has an ID number")) )
vAR_g.add( (vAR_ex.hasID, RDFS.domain, vAR_ex.Student) )
vAR_g.add( (vAR_ex.hasID, RDFS.range, XSD.integer) )

vAR_g.add( (vAR_ex.hasTopic, RDF.type, RDF.Property) )
vAR_g.add( (vAR_ex.hasTopic, RDFS.label, Literal("hasTopic", lang="en")) )
vAR_g.add( (vAR_ex.hasTopic, RDFS.comment, Literal("Course has a topic")) )
vAR_g.add( (vAR_ex.hasTopic, RDFS.domain, vAR_ex.Course) )
vAR_g.add( (vAR_ex.hasTopic, RDFS.range, vAR_ex.Topic) )

vAR_g.add( (vAR_ex.hasCompleted, RDF.type, RDF.Property) )
vAR_g.add( (vAR_ex.hasCompleted, RDFS.label, Literal("hasCompleted", lang="en")) )
vAR_g.add( (vAR_ex.hasCompleted, RDFS.comment, Literal("Student has completed a course")) )
vAR_g.add( (vAR_ex.hasCompleted, RDFS.domain, vAR_ex.Student) )
vAR_g.add( (vAR_ex.hasCompleted, RDFS.range, vAR_ex.Course) )

vAR_g.add( (vAR_ex.hasGrade, RDF.type, RDF.Property) )
vAR_g.add( (vAR_ex.hasGrade, RDFS.subPropertyOf, vAR_ex.hasCompleted) )
vAR_g.add( (vAR_ex.hasGrade, RDFS.label, Literal("hasGrade", lang="en")) )
vAR_g.add( (vAR_ex.hasGrade, RDFS.comment, Literal("Student has a grade for a completed course")) )
vAR_g.add( (vAR_ex.hasGrade, RDFS.domain, vAR_ex.hasCompleted) )
vAR_g.add( (vAR_ex.hasGrade, RDFS.range, XSD.string ) )

# processing university_data data into RDF triples
with open("D:\\ConvAI\\DSAI_University_Data_1") as data:
    file = csv.reader(data, delimiter=',')
    for row in file:
        university = URIRef(exdata + row[0].replace(" ", "_")) # define university URI using first column
        link = URIRef(row[1]) # define link URI to university's entry in dbpedia using second column

        vAR_g.add( (university, RDF.type, vAR_ex.University) )
        vAR_g.add( (university, FOAF.name, Literal(row[0])) )
        vAR_g.add( (university, RDFS.seeAlso, link) )

# processing course data into RDF triples
with open("D:\\ConvAI\\DSAI_Course_Data_1") as data:
    file = csv.reader(data, delimiter=',')
    for row in file:
        course = URIRef(exdata + row[0].replace(" ", "_")) # define course URI using first column
        link = URIRef(row[3]) # define link URI to online source of course using fourth column

        vAR_g.add( (course, RDF.type, vAR_ex.Course) )
        vAR_g.add( (course, FOAF.name, Literal(row[0])) )
        vAR_g.add( (course, vAR_ex.hasSubject, Literal(row[1])) )
        vAR_g.add( (course, vAR_ex.hasNumber, Literal(row[2])) )
        vAR_g.add( (course, RDFS.seeAlso, link) )

        try:
            # use dbpedia spotlight to find topics
            topics = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate',row[0],confidence=0.2, support=20)

            # process topics of course into RDF triples
            for topicRow in topics:
                print(topicRow)
                topic = URIRef(exdata + topicRow['surfaceForm'].replace(" ", "_")) # define topic URI using topic's surfaceForm from result
                topicLink = URIRef(topicRow['URI']) # define link URI to dbpedia source of the topic

                # only add topic to graph if not already in graph
                for s, p, o in vAR_g:
                    if not (topic, RDF.type, vAR_ex.Topic) in vAR_g:
                        vAR_g.add( (topic, RDF.type, vAR_ex.Topic) )
                        vAR_g.add( (topic, FOAF.name, Literal(topicRow['surfaceForm'])) )
                        vAR_g.add( (topic, RDFS.seeAlso, topicLink) )

                # add topic to this course
                vAR_g.add( (course, vAR_ex.hasTopic, topic))
        except:
            print()


# processing student data into RDF triples
with open("D:\\ConvAI\\DSAI_Student_Data_1") as data:
    file = csv.reader(data, delimiter=',')
    for row in file:
        student = URIRef(exdata + row[0].replace(" ", "_")) # define student URI using first column
        course = URIRef(exdata + row[3].replace(" ", "_")) # define course URI using fourth column

        # only add student to graph if not already in graph
        for s, p, o in vAR_g:
            if not (student, RDF.type, vAR_ex.Student) in vAR_g:
                vAR_g.add( (student, RDF.type, vAR_ex.Student) )
                vAR_g.add( (student, FOAF.name, Literal(row[0])) )
                vAR_g.add( (student, vAR_ex.hasID, Literal(row[1])) )
                vAR_g.add( (student, FOAF.mbox, Literal(row[2])) )

                if not (row[3] == ''):
                    vAR_g.add( (student, vAR_ex.hasCompleted, course) )
                if not (row[4] == ''):
                    vAR_g.add( (vAR_ex.hasCompleted, vAR_ex.hasGrade, Literal(row[4])) )
            else:
                if not (row[3] == ''):
                    vAR_g.add( (student, vAR_ex.hasCompleted, course) )
                if not (row[4] == ''):
                    vAR_g.add( (vAR_ex.hasCompleted, vAR_ex.hasGrade, Literal(row[4])) )

# print graph in N-Triples format to knowledge_base.nt file
# run this only once to populate the .nt file
print(vAR_g.serialize("D:\\DSAI_Conversational_AI\\Knowledge_Graph\\Utility\\DSAI_Knowledge_Base.nt", format="nt"))