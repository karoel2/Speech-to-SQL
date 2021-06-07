from settings import MicrophoneStream, listen_print_loop
from google.cloud import speech_v1p1beta1 as speech
import ply.lex as lex

RATE = 16000
CHUNK = int(RATE / 10)

def main():
    temp = ''
    language_code = "pl-PL"

    with open('data.txt', 'r') as file:
        phrases = []
        for line in file:
            phrases.append(line.rstrip())

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        speech_contexts = [{
        'phrases': phrases,
        'boost': 20
        }]
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        temp = listen_print_loop(responses)
    return temp


text = ''
text = main().replace('stop', '').lower()

TABLES = [r'pacjenci', r'wizyty', r'pacjenta', r'lekarze']
COLUMNS = [r'id\spacjenta', r'nazwisko', r'imie', r'pesel', r'data\surodzenia', r'lekarz', r'pacjent', r'koszt', r'data\swizyty', r'id\slekarza', r'specjalnosc', r'nip']

def create_regex(table):
    str = r''
    for item in table:
        str += f'|({item})'
    return str[1:]

TABLES_STR = create_regex(TABLES)
COLUMNS_STR = create_regex(COLUMNS)

tokens = (
'SELECT',
'ALL',
'DISTINCT',
'TOP',
'PERCENT',
'PROPER_NAME',
'DOT',
'MIN',
'MAX',
'COUNT',
'AVG',
'SUM',
'FROM',
'WHERE',
'AND',
'OR',
'NOT',
'IS',
'EQUAL',
'GREATER_THAN',
'LESS_THAN',
'GREATER_THAN_OR_EQUAL',
'LESS_THAN_OR_EQUAL',
'NOT_EQUAL',
'BEGINE',
'END',
'ORDER_BY',
'ASC',
'DESC',
'TABLE',
'COLUMN',
'HAVING',
'GROUP_BY',
'JOIN',
'ON',
'INNER_JOIN',
'LEFT_JOIN',
'RIGHT_JOIN',
'FULL_OUTER_JOIN',
'NULL',
'IN',
'NUMBER'
)

t_SELECT = r'(wybierz)|(zaznacz)|(podaj)|(zwróć)'
t_ALL = r'(wszystkie)|(wszystko)'
t_DISTINCT = r'(unikalne)|(wyjątkowe)'
t_TOP = r'(pierwsze)|(górne)|(początkowe)'
t_PERCENT = r'procent'

t_DOT = r'(kropka)|(\.)'
t_MIN = r'minimum(\sz)?'
t_MAX = r'maksimum(\sz)?'
t_COUNT = r'(policz)|(ilość)|(oblicz\silość)'
t_AVG = r'(średnia)|(oblicz\sśrednią)'
t_SUM = r'(suma)|(zsumuj)|(oblicz\ssumę)'

t_FROM = r'(z\stabeli)|(z\sbazy\sdanych)'

t_WHERE = r'(gdzie)|(tam\sgdzie)'
t_AND = r'oraz'
t_OR = r'(lub)|(albo)'
t_NOT = r'(nieprawda\sże)|(nie\sjest)'
t_IS = r'jest'

t_EQUAL	= r'(jest\s)?równ(a|e|y)'
t_GREATER_THAN = r'(jest\s)?większ(a|e)\s(niż)?'
t_LESS_THAN	= r'(jest\s)?mniejsz(a|e)\s(niż)?'
t_GREATER_THAN_OR_EQUAL = r'(jest\s)?większ(a|e)\s(albo)|(lub)|(bądź)\s(jest\s)?równ(a|e)\s(niż)?'
t_LESS_THAN_OR_EQUAL = r'(jest\s)?mniejsz(a|e)\s(albo)|(lub)|(bądź)\s(jest\s)?równ(a|e)\s(niż)?'
t_NOT_EQUAL = '(jest\s)?różne\s(od)?'

t_BEGINE = r'((rozpocznij)|(zacznij)|(stwórz))\spodzapytanie'
t_END = r'((zakończ)|(zamknij))\spodzapytanie'

t_ORDER_BY = r'(posortuj(\spo)?)|(uporządkuj(\spo)?)|(ułóż\sw\skolejności)'
t_ASC = r'rosnąco'
t_DESC = r'malejąco'

t_TABLE = create_regex(TABLES)
t_COLUMN = create_regex(COLUMNS)

t_HAVING = r'(mając(e|y)?)|(posiadają(c|e)?)'

t_GROUP_BY = r'pogrupuj(\spo)?'

t_JOIN = r'(połącz(enie)?)|(złącz(enie)?)'
t_ON = r'na'
t_INNER_JOIN = r'((połącz(enie)?)|(złącz(enie)?))\s(wewnętrzne)'
t_LEFT_JOIN = r'((połącz(enie)?)|(złącz(enie)?))\s(lewostronn(i)?e)'
t_RIGHT_JOIN = r'((połącz(enie)?)|(złącz(enie)?))\s(prawostronne)'
t_FULL_OUTER_JOIN = r'((połącz(enie)?)|(złącz(enie)?))\s(całkowite)'

t_NULL = r'((bez)|(brak)|(nie\sma))\swartości'
t_IN = r'w'

def t_NUMBER(t):
    r'\d+(,\d+)?'
    if ',' in t.value:
        t.value = int(t.value)
    else:
        t.value = int(t.value)
    return t

def t_PROPER_NAME(t):
    r'nazwa\swłasna\s\w+'
    t.value = t.value[13:]
    return t


t_ignore  = ' \t\n'

def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

lexer = lex.lex()

lexer.input(text)

#EXAMPLES
"""
lexer.input('''Zaznacz suma koszt
                Z tabeli wizyty Gdzie pacjent jest równy
                stwórz podzapytanie zaznacz id pacjenta
                Z tabeli pacjenci gdzie
                Nazwisko jest równe nazwa własna Gumowska
                oraz imie jest równe nazwa własna anna
                zakończ podzapytanie'''.lower())

lexer.input('''Wybierz nazwisko z tabeli pacjenci
                połącz lewostronnie wizyty na pacjenci
                kropka id pacjenta jest równe wizyty
                kropka pacjent Gdzie wizyty
                kropka pacjent jest bez wartości'''.lower())

lexer.input('''zaznacz unikalne lekarze kropka nazwisko
                lekarze kropka specjalnosc
                z tabeli lekarze
                Połącz  wizyty
                Na lekarze kropka id lekarza równe wizyty kropka lekarz
                Złącz pacjenci
                Na pacjenci kropka id pacjenta równe wizyty kropka pacjent
                Gdzie pacjent kropka nazwisko równe nazwa własna Witkowski'''.lower())

lexer.input('''Zaznacz nazwisko specjalnosc
                Z tabeli lekarze
                Gdzie specjalnosc jest równa rozpocznij podzapytanie wybierz specjalnosc z tabeli lekarze gdzie nazwisko jest równe nazwa własna Stefanowicz zakończ podzapytanie
                Oraz nazwisko jest różne od  nazwa własna Stefanowicz'''.lower())
"""
lista = []
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
    lista.append(tok)

lista.append(None)

breaks = [
'FROM',
'JOIN',
'INNER_JOIN',
'LEFT_JOIN',
'RIGHT_JOIN',
'FULL_OUTER_JOIN',
'WHERE',
'GROUP_BY',
'HAVING',
'SELECT',
'OREDR_BY',
'BEGINE',
]


if lista[0] != None:
    it = iter(lista)
    item = next(it)
    line = []
    commands = []
    before = ' '


    while item != None:
        if item.type == 'END':
            commands.append(line)
            line = [item.type]
            commands.append(line)
            line =[]
            item = next(it)
        elif item.type in breaks:
            commands.append(line)
            line = [(item.type).replace('_', ' ')]
            item = next(it)
        elif item.type == 'TABLE':
            before = item.value
            item = next(it)
            if item == None:
                line.append(before.replace(' ', '_'))
                break
            if item.type == 'DOT':
                item = next(it)
                if item == None:
                    line.append(before.replace(' ', '_'))
                    break
                if item.type == 'COLUMN':
                    line.append(f'{before}.{(item.value)}'.replace(' ', '_'))
                    before = ' '
                    item = next(it)
                else:
                    line.append('ERR' + f'{before}.{(item.value)}'.replace(' ', '_'))
            else:
                line.append(before.replace(' ', '_'))
                before = ' '
        elif item.type == 'COLUMN':
            line.append((item.value).replace(' ', '_'))
            item = next(it)
        elif item.type == 'NUMBER':
            line.append(item.value)
            item = next(it)
        elif item.type == 'PROPER_NAME':
            line.append(('\'' + item.value + '\'').replace(' ', '_'))
            item = next(it)
        elif item.type == 'EQUAL':
            line.append('=')
            item = next(it)
        elif item.type == 'GREATER_THAN':
            line.append('>')
            item = next(it)
        elif item.type == 'LESS_THAN':
            line.append('<')
            item = next(it)
        elif item.type == 'GREATER_THAN_OR_EQUAL':
            line.append('>=')
            item = next(it)
        elif item.type == 'LESS_THAN_OR_EQUAL':
            line.append('<=')
            item = next(it)
        elif item.type == 'NOT_EQUAL':
            line.append('!=')
            item = next(it)
        elif item.type == 'ALL':
            line.append('*')
            item = next(it)
        elif item.type == 'PERCENT':
            line.append('PERCENT')
            item = next(it)
        elif item.type in ['MIN', 'MAX', 'COUNT', 'AVG', 'SUM']:
            func = item.type
            item = next(it)
            if item == None:
                break
            if item.type == 'COLUMN':
                line.append(f'{func}({item.value})')
                item = next(it)
        else:
            line.append(item.type)
            item = next(it)
    commands.append(line)
print(*commands, sep='\n')

final = []
tab = []
for item in commands[1:]:
    if item:
        if item[0] == 'BEGINE':
            final.append(tab + [[' ( ']])
            tab = []
        elif item[0] == 'END':
            final.append(tab + [[' ) ']])
            tab = []
        else:
            tab.append(item)
final.append(tab)
for item in final:
    print(*item,sep='\n',end='\n\n')

querry = []
for line in final:
    for item in line:
        temp = ''
        if item[0] == 'SELECT' or item[0] == 'FROM':
            for it in item:
                if isinstance(item, str):
                    temp += ' ' + it + ','
                else:
                    temp += ' ' + str(it)

            if 'TOP' in temp:
                temp = temp.replace(',', '', 1)
            if 'DISTINCT' in temp:
                querry.append(temp[0:].replace(',', '', 2).replace(' ', '', 1))
            else:
                querry.append(temp[0:].replace(',', '', 1).replace(' ', '', 1))
        else:
            for it in item:
                temp += ' ' + it
            querry.append(temp.replace(' ', '', 1))
querry[-1] += ';'
print(*querry,sep='\n')
