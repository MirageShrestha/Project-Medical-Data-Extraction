from backend.src.parser_prescription import PrescriptionParser
import pytest

@pytest.fixture()
def doc_1_maria():
    document_text = '''
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
    return PrescriptionParser(document_text)

@pytest.fixture()
def doc_2_rachel():
    document_text = '''
    Dr John Smith, M.D
    2 Non-Important Street,
    New York. Phone (000)-111-2222

    Name: Rachel Shrestha Date: 5/11/2022

    Address: Shantinagar

    K

    Prednisone 20 mg
    Lialda 2.4 gram

    Directions:
    Prednisone, Taper 5 mg every 3 days,

    Finish in 2.5 weeks
    Lialda - take 2 pill everyday for 1 month

    Refill: 3. times
    '''
    return  PrescriptionParser(document_text)

@pytest.fixture()
def doc_3_empty():
    return PrescriptionParser('')



def test_get_name(doc_1_maria, doc_2_rachel, doc_3_empty):
    assert doc_1_maria.get_field('patient_name') == 'Marta Sharapova'
    assert doc_2_rachel.get_field('patient_name') == 'Rachel Shrestha'
    assert doc_3_empty.get_field('patient_name') == None

def test_get_address(doc_1_maria, doc_2_rachel, doc_3_empty):
    assert doc_1_maria.get_field('patient_address') == '9 tennis court, new Russia, DC'
    assert doc_2_rachel.get_field('patient_address') == 'Shantinagar'
    assert doc_3_empty.get_field('patient_address') == None

def test_get_medicines(doc_1_maria, doc_2_rachel, doc_3_empty):
    assert doc_1_maria.get_field('medicines') == 'Prednisone 20 mg\n    Lialda 2.4 gram'
    assert doc_2_rachel.get_field('medicines') == 'Prednisone 20 mg\n    Lialda 2.4 gram'
    assert doc_3_empty.get_field('medicines') == None

def test_get_directions(doc_1_maria, doc_2_rachel, doc_3_empty):
    assert doc_1_maria.get_field('direction') == ('Prednisone, Taper 5 mg every 3 days,\n'
 '\n'
 '    Finish in 2.5 weeks\n'
 '    Lialda - take 2 pill everyday for 1 month')
    assert doc_2_rachel.get_field('direction') == ('Prednisone, Taper 5 mg every 3 days,\n'
 '\n'
 '    Finish in 2.5 weeks\n'
 '    Lialda - take 2 pill everyday for 1 month')
    assert doc_3_empty.get_field('direction') == None

def test_get_refill(doc_1_maria, doc_2_rachel, doc_3_empty):
    assert doc_1_maria.get_field('refill') == '2.'
    assert doc_2_rachel.get_field('refill') == '3.'
    assert doc_3_empty.get_field('refill') == None

def test_parse(doc_1_maria, doc_2_rachel, doc_3_empty):
    record_maria = doc_1_maria.parse()
    assert record_maria['patient_name']=='Marta Sharapova'
    assert record_maria['patient_address'] =='9 tennis court, new Russia, DC'
    assert record_maria['medicines'] == 'Prednisone 20 mg\n    Lialda 2.4 gram'
    assert record_maria['direction'] == ('Prednisone, Taper 5 mg every 3 days,\n'
 '\n'
 '    Finish in 2.5 weeks\n'
 '    Lialda - take 2 pill everyday for 1 month')
    assert record_maria['refill'] == '2.'

    record_rachel = doc_2_rachel.parse()
    assert record_rachel == {
            'patient_name': 'Rachel Shrestha',
            'patient_address':'Shantinagar',
            'medicines':'Prednisone 20 mg\n    Lialda 2.4 gram',
            'direction':('Prednisone, Taper 5 mg every 3 days,\n'
 '\n'
 '    Finish in 2.5 weeks\n'
 '    Lialda - take 2 pill everyday for 1 month'),
            'refill':'3.'
        }
    record_empty = doc_3_empty.parse()
    assert record_empty== {
            'patient_name': None,
            'patient_address':None,
            'medicines':None,
            'direction':None,
            'refill':None
        }

