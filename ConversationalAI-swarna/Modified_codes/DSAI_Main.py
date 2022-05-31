#import libraries
from rdflib import Graph, Literal
import re
import random

vAR_responses = [
  [r'What is the name of the organization?',
  [  "%1"]],

  [r'Which use cases did (.*) take?',
  [  "%1"]],

  [r'Which use cases cover (.*)?',
  [  "%1"]],

  [r'Who is familiar with (.*)?',
  [  "%1"]],

  [r'How many students have enrolled in total?',
  [ "%1"]],

  [r'How many usecases available?',
  [ "%1"]],

  [r'quit',
  [  "Thank you for your questions.",
    "Goodbye!",
    "Thank you, that will be $100.  Have a good day!"]],

  [r'(.*)',
  [  "Please ask a question related to the university.",
    "Can you elaborate on that?",
    "I see. Do you have a question?",
    "Please ask questions about courses, students and topics."]]
]

class Chatbot:
    def __init__(self):
        #constructor
        self.vAR_g = Graph() #graph object
        self.vAR_g.parse("D:\\ConvAI\\DSAI_Knowledge_Base_1.nt", format="nt") #parse .nt file

        self.keys = list(map(lambda x:re.compile(x[0], re.IGNORECASE),vAR_responses))
        self.values = list(map(lambda x:x[1],vAR_responses))

    def get_org(self):
        kl = re.search("what is the name of the organization?", self.vAR_str)
        if kl:
            vAR_res = self.vAR_g.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ex: <http://example.org/>
            SELECT ?Organization
            WHERE {
                ?Organization rdf:type ex:Organization
            }
            """)

            for vAR_row in vAR_res:
                vAR_row = vAR_row[0].split('#')[1]
                self.vAR_result += vAR_row + '\n'

    def get_use_case(self):
        kl = re.search("which use cases did (.*) take?", self.vAR_str)
        if kl:
            vAR_student = self.vAR_match.group(self.vAR_num)
            vAR_res = self.vAR_g.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ex: <http://example.org/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT DISTINCT ?subject ?number ?name
                WHERE {
                    ?student foaf:name ?studentName .
                    ?student ex:hasEnrolled ?course .
                    ?course ex:hasSubject ?subject .
                    ?course ex:hasNumber ?number .
                    ?course foaf:name ?name .
                }
            """, initBindings={'studentName': Literal(vAR_student)})
            if not vAR_res:
                self.vAR_result = vAR_student + ' did not take any courses!'
            else:
                for vAR_row in vAR_res:
                    self.vAR_result += vAR_row[0] + ' ' + vAR_row[1] + ' ' + vAR_row[2] + '\n'

    def get_subject(self):
        kl = re.search("which use cases cover (.*)", self.vAR_str)
        if kl:
            vAR_topic = self.vAR_match.group(self.vAR_num)
            vAR_topic = vAR_topic.split('?')[0]
            vAR_res = self.vAR_g.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX ex: <http://example.org/>
            SELECT ?subject ?number ?name
                WHERE {
                    ?course ex:hasSubject ?subject .
                    ?course ex:hasNumber ?number .
                    ?course foaf:name ?name .
                }
            """, initBindings={'subject': Literal(vAR_topic)})
            
            if not vAR_res:
                self.vAR_result = 'There are no courses that cover ' + vAR_topic + '!'
            else:
                for vAR_row in vAR_res:
                    self.vAR_result += vAR_row[2] + ' ' + vAR_row[1] + ' ' + vAR_row[0] + '\n'

    def get_stud_subject(self):
        kl = re.search("[wW]ho is familiar with (.*)", self.vAR_str)
        if kl:
            vAR_topic = self.vAR_match.group(self.vAR_num)
            vAR_topic = vAR_topic.split('?')[0]
            vAR_res = self.vAR_g.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ex: <http://example.org/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT DISTINCT ?name
                WHERE {
                    ?student ex:hasEnrolled ?course .
                    ?student foaf:name ?name .
                }
            """, initBindings={'subject': Literal(vAR_topic)})
            if not vAR_res:
                self.vAR_result = 'There are no students that are familiar with ' + vAR_topic + '!'
            else:
                for vAR_row in vAR_res:
                    if 'http' not in vAR_row[0]:
                        self.vAR_result += vAR_row[0] + '\n'

    def get_stud_total(self):
        kl = re.search("how many students have enrolled in total", self.vAR_str)
        if kl:
            vAR_res = self.vAR_g.query("""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ex: <http://example.org/>
                SELECT (COUNT(?student) as ?count)
                    WHERE {
                        ?student rdf:type ex:Student
                    }
                """)
            if not vAR_res:
                self.vAR_result = 'There are no students enrolled yet!' + vAR_topic + '!'
            else:
                for vAR_row in vAR_res:
                    self.vAR_result += vAR_row[0] + '\n'

    def get_use_case_total(self):
        kl = re.search('how many usecases available?',self.vAR_str)
        if kl:
            vAR_res = self.vAR_g.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ex: <http://example.org/>
            SELECT (COUNT(?Use_case) as ?count)
            WHERE {
                ?Use_case rdf:type ex:Use_case
            }
            """)
            if not vAR_res:
                self.vAR_result = 'There are no use cases available right now!' + vAR_topic + '!'
            else:
                for vAR_row in vAR_res:
                    self.vAR_result += vAR_row[0] + '\n'

    def respond(self,vAR_str):
        #method to find response for input sentence
        for i in range(0, len(self.keys)):
            # print(self.keys)
            self.vAR_match = self.keys[i].match(vAR_str)
            if self.vAR_match:
                vAR_resp = random.choice(self.values[i])
                vAR_pos = vAR_resp.find('%')
                while vAR_pos > -1:
                    self.vAR_num = int(vAR_resp[vAR_pos+1:vAR_pos+2])
                    self.vAR_result = ''
                    self.vAR_str = vAR_str.lower()

                    self.get_org()

                    self.get_use_case()

                    self.get_subject()

                    self.get_stud_subject()

                    self.get_stud_total()

                    self.get_use_case_total()

                    vAR_resp = vAR_resp[:vAR_pos] + \
                        self.vAR_result + \
                        vAR_resp[vAR_pos+2:]

                    vAR_pos = vAR_resp.find('%')

                if vAR_resp[-2:] == '?.': vAR_resp = vAR_resp[:-2] + '.'
                if vAR_resp[-2:] == '??': vAR_resp = vAR_resp[:-2] + '?'
                return vAR_resp
                
    def run_all(self):
        print('-' * 100)
        print('Welcome to DSAI Chatbot! Please enter your question and enter "quit" to end the conversation.')
        print('-'*100)

        vAR_s = '' 
        while vAR_s != 'quit': 
            try:
                vAR_s = input('> ')
            except EOFError:
                vAR_s = 'quit'
            while vAR_s[-1] in '!.':
                vAR_s = vAR_s[:-1]
            print(self.respond(vAR_s))

vAR_obj = Chatbot()
vAR_obj.run_all()