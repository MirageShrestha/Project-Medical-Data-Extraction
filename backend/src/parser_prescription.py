import re

from backend.src.parser_generic import MedialDocParser

class PrescriptionParser(MedialDocParser):
    def __init__(self, text):
        MedialDocParser.__init__(self, text)

    def parse(self):
        return {
            'patient_name': self.get_field('patient_name'),
            'patient_address':self.get_field('patient_address'),
            'medicines':self.get_field('medicines'),
            'direction':self.get_field('direction'),
            'refill':self.get_field('refill')
        }

    def get_field(self, field_name):
        pattern = ''
        flags =None

        pattern_dict ={
            'patient_name': {'pattern': 'Name:(.*)Date:', 'flags':0},
            'patient_address': {'pattern': 'Address:(.*)\n', 'flags':0},
            'medicines': {'pattern': 'K(.*)Directions', 'flags':re.DOTALL} ,
            'direction': {'pattern': 'Directions:(.*)Refill', 'flags':re.DOTALL},
            'refill': {'pattern': 'Refill:(.*)times', 'flags':0}
        }

        pattern_object = pattern_dict.get(field_name)
        if pattern_object:
            matches = re.findall(pattern_object['pattern'], self.text, flags = pattern_object['flags'])
            if len(matches) > 0:
                return matches[0].strip()

    '''CODE REFRACTORING'''
    # def get_name(self):
    #     pattern = 'Name:(.*)Date:'
    #     matches = re.findall(pattern, self.text)
    #     if len(matches)>0:
    #         return matches[0].strip()
    #
    # def get_address(self):
    #     pattern = 'Address:(.*)\n'
    #     matches = re.findall(pattern, self.text)
    #     if len(matches) > 0:
    #         return matches[0].strip()
    #
    # def get_medicines(self):
    #     pattern = 'K(.*)Directions'
    #     matches = re.findall(pattern, self.text, flags=re.DOTALL)
    #     if len(matches) > 0:
    #         return matches[0].strip()
    #
    # def get_directions(self):
    #     pattern = 'Directions:(.*)Refill'
    #     matches = re.findall(pattern, self.text, flags=re.DOTALL)
    #     if len(matches) > 0:
    #         return matches[0].strip()
    #
    # def get_refill(self):
    #     pattern = 'Refill:(.*)times'
    #     matches = re.findall(pattern, self.text)
    #     if len(matches) > 0:
    #         return matches[0].strip()

if __name__ == '__main__':
    document_text='''
    Dr John Smith, M.D
2 Non-Important Street,
New York. Phone (000)-111-2222

Name: Marta Sharapova Date: 5/11/2022

Address: 9 tennis court, new Russia, DC

K

Prednisone 20 mg
Lialda 2.4 gram

Directions:
Prednisone, Taper 5 mg every 3 days,

Finish in 2.5 weeks
Lialda - take 2 pill everyday for 1 month

Refill: 2. times'''
    pp = PrescriptionParser(document_text)
    print(pp.parse())