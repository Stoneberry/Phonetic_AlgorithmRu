import re
import pandas as pd


__data__ = pd.read_csv('phon_data/data.csv', index_col='Unnamed: 0')
__vows__ = pd.read_csv('phon_data/vows.csv', sep=',', index_col='name')
__aff__ = pd.read_csv('phon_data/aff_.csv', sep=',', index_col='name')
__cons__ = pd.read_csv('phon_data/cons_.csv', sep=',', index_col='name')
__st_words__ = pd.read_csv('phon_data/stress_data.csv', index_col='word')
__stop_words__ = ['а',  'без',  'близ',  'в',  'вне',  'во',  'вокруг',  'вслед',  'для',  'до',  'за',  'и',  'из',
              	  'изза',  'изо',  'изпод',  'к',  'ко',  'меж',  'между',  'мимо',  'на',  'над',  'о',  'об',  'обо',
              	  'около',  'от',  'ото',  'перед',  'передо',  'по', 'поверх',  'под',  'подо',  'понад',  'после',
             	  'пред',  'при',  'про',  'ради',  'с',  'сверх',  'сверху']


def __tokenize__(text):
    """
        Функция удаляет все знаки препинания.
    """
    text = re.sub(r'[^\w\s]', '', text).replace('\n', '')
    text = re.sub(r'[\s]{2,}', ' ', text)
    return text.split(' ')


def __num_of_vowls__(word):
    """
	Функция считает кол-во гласных в слове
	
	>>> __num_of_vowls__('мама')
	2
    """
    num = len(re.findall('(а|е|ё|о|и|я|ю|у|ы|э)', word))
    if num:
        return num
    else:
        return 1


def __stressed__(word):
    """
	Функция определяет ударение в слове по словарю.
	Если слова в словаре нет, выдаются все возможные варианты.
	
	>>> [i for i in stressed('замок', st_words)]
	[2, 1]
    """

    try:
        a = __st_words__.loc[word]['stressed_s'].tolist()

        if isinstance(a, list):
            yield from a
        else:
            yield from [a]

    except KeyError:
        yield from ['None']
        

def __change__(word):
	"""
	Замена сочетаний согласных
    """
    word = re.sub('(с|ст|сс|з|зд|ж|ш)ч', 'щ', word)
    word = re.sub('(с|зд|з)щ', 'щ', word)
    word = re.sub('(тч|тш|дш)', 'ч', word)
    word = re.sub('(с|з)ш', 'ш', word)
    word = re.sub('сж', 'ж', word)
    word = re.sub('(т|ть|д)с', 'ц', word)
    word = re.sub('(ст|сть)с', 'ц', word)
    return word
    

def __my_type__(letter):
    """
	Функция определяет тип входного символа: гласная, согласная, знак
    """
    if letter in vows.index:
        return 'v'
    
    if letter in cons.index:
        return 'c'
    
    if letter in ('ь', 'ъ'):
        return 'm'
    else:
        raise ValueError('Not Cyrillic')



def __due_to_vow_table__(ans, index, letter, stress, vow_n, length):
    """
	Функция преобразует гласные буквы в звуки в зависимости от позиции
    """

    if vow_n == stress:  # ударный

        if ans.value not in ('а', 'о', 'у', 'ы') and ans.next is not None and ans.next.type == 'c':

            if ans.value != 'э' and ans.next.value not in ('ш', 'ж', 'ц'):
                ans.next.soft = True
            elif ans.value in ('э', 'е') and ans.next.value in ('ш', 'ж', 'ц'):
                letter = 'э'
            elif ans.value == 'и':
                letter = 'ы'

        j(ans, letter, length, index, 'V')

    elif index == length - 1:  # начало
        j(ans, letter, length, index, '#')

    elif vow_n == stress + 1:  # первый предударный

        if ans.next is not None and ans.next.value in ('ц', 'ж', 'ш'):
            ans.value = vows.loc[letter]['v1_sh']

        elif letter in ('е', 'ё', 'и', 'ю', 'я'):
            ans.value = vows.loc[letter]['v1_soft']
            ans.next.soft = True
        else:
            ans.value = vows.loc[letter]['v1_hard']

    elif vow_n >= stress + 2:  # второй предударный

        if ans.next is not None and ans.next.value in ('ц', 'ж', 'ш'):
            ans.value = vows.loc[letter]['v2_hard']

        elif ans.next is not None and ans.next.type == 'v':
            if letter in ('е', 'ё', 'и', 'ю', 'я'):
                ans.value = vows.loc[letter]['v1_soft']
            else:
                ans.value = vows.loc[letter]['v1_hard']

        elif letter in ('е', 'ё', 'и', 'ю', 'я'):
            ans.value = vows.loc[letter]['v2_soft']
            ans.next.soft = True
        else:
            ans.value = vows.loc[letter]['v2_hard']

    elif vow_n < stress:  # заударные

        if ans.next is not None and ans.next.value in ('ц', 'ж', 'ш'):

            j(ans, letter, length, index, 'vn_hard')

        elif letter in ('е', 'ё', 'и', 'ю', 'я'):

            if vow_n == stress - 1 and ans.next is not None and ans.next.type == 'v':
                j(ans, letter, length, index, 'vn_soft')
            else:
                ans.value = vows.loc[letter]['vn_soft']
            ans.next.soft = True

        else:
            if vow_n == stress - 1 and ans.next is not None and ans.next.type == 'v':
                j(ans, letter, length, index, 'vn_hard')
            else:
                ans.value = vows.loc[letter]['vn_hard']



def __j__(ans, letter, length, index, position):
    """
	Функция вставляет й в нужной позиции
    """

    ans.value = vows.loc[letter][position]

    if letter in ('ю', 'е', 'ё', 'я'):

        if index == length - 1:
            ans.j_ = True

        elif ans.next is not None and ans.next.type == 'v':
            ans.j_ = True

            if 'vn' in position:
                ans.value = vows.loc[letter]['vn_hard']

        elif ans.next is not None and ans.next.value in ('ь', 'ъ'):
            ans.j_ = True

            if 'vn' in position:
                ans.value = vows.loc[letter]['vn_hard']

    elif letter in ('и', 'о') and ans.next is not None and ans.next.value == 'ь':
        ans.j_ = True

        if 'vn' in position:
                ans.value = vows.loc[letter]['vn_hard']


def __cons_tranformer__(ans, letter, vcd=False):
    """
	Функция преобразует согласные буквы в звуки в зависимости от позиции
    """
	
    a = letter

    if letter in ('ч', 'ш', 'щ', 'ж'):
        ans.value = cons.loc[ans.value]['hard']
        if ans.__dict__.__contains__('soft'):
            del ans.soft
        if letter in ('ч', 'щ'):
            if ans.__dict__.__contains__('no_voice'):
                del ans.no_voice
            if ans.__dict__.__contains__('voice'):
                del ans.voice

    if ans.__dict__.__contains__('no_voice'):  # оглушение
        ans.value = cons.loc[ans.value]['no_voice']

    elif ans.__dict__.__contains__('voice'):  # озвончение
        ans.value = cons.loc[ans.value]['voiced']

    if vcd is True:
        if ans.previous is None:
            ans.value = cons.loc[ans.value]['voiced']

    if not vcd:
        if ans.previous is None:  # конец слова
            if ans.next is not None:
                ans.next.no_voice = True
            if data[ans.value]['vcd'] == '+':
                ans.value = cons.loc[ans.value]['no_voice']

    if ans.next is not None:
        if ans.value in data.columns and data[ans.value]['vcd'] == '-' and ans.next is not None:  # оглушение следующих

            if ans.next.value in data.columns and data[ans.next.value]['son'] == '-':
                ans.next.no_voice = True

        elif ans.value in data.columns and data[ans.value]['son'] == '-' and ans.value not in ('в', "в’") and data[ans.value]['vcd'] == '+':  # озвончение слудующих
            ans.next.voice = True

    if ans.previous is not None:

        if ans.previous.value == 'к' and letter == 'г':
            ans.value = 'х'

        elif ans.previous.value in (ans.value, ans.value + "’"):
            ans.value = ''

    if ans.__dict__.__contains__('soft'):  # смягчение
        ans.value = cons.loc[ans.value]['soft']


class Node(object):
    def __init__(self, value=''):
        self.value = value
        self.type = None
        self.previous = None
        self.next = None


def transcription(word, stress=1, next_word=False, stop_word=False, separate=True, stop=False, vcd=False):

    """
    Фунция, которая определяет фонетическую транскриацию для
    слова с заданным ударением, расчитываемым с конца слова.

    Функция принимает 3 аргемента:
    i - type int, номер гласного, на который падает ударение
    (отсчет производится с конца слова).
    word - type str, слово, для которого должен произвожится разбор.

    >>> transcription(2, 'мама')
    ['м', 'а', 'м', 'ъ']

    >>> transcription(1, 'мама')
    ['м', 'а', 'м', 'а']
	
	>>> transcription('съехать', stress=2, separate=False)
	'сjехът’'

    Функция работает только с кириллическими символами. Если в слове содержатся не кириллические символы, вызывается ошибка.

    >>> transcription(2, 'papa')
    Traceback (most recent call last):
        ...
    ValueError: No vowles or not Cyrillic elements


    Если пользователь указывает номер гласной меньший кол-ва гласных,
    вызывается ошибка.

    >>> transcription(3, 'мама')
    Traceback (most recent call last):
        ...
    ValueError: There are only 2 vowel(s)
    """

    if not isinstance(word, str):
        raise ValueError('Wrong data type')

    if not isinstance(stress, int):
        raise ValueError('Wrong data type')

    word = tokenize(word)

    if len(word) > 1:
        raise ValueError('Enter a word, not a phrase')

    word = word[0]
    nums = num_of_vowls(word)

    if stress:
        if nums < stress or stress < -1:
            raise ValueError('There are only {} vowel(s)'.format(str(num_of_vowls(word))))

    if not stress:
        stress = nums//2 + 1

    if stop is True:
        stress = -1

    word = word.lower()
    letters = list(__change__(word))[::-1]

    ans = Node()
    head = ans
    prev = ans
    answer = []
    special = False
    length = len(letters)
    vow_n = 0

    for index, letter in enumerate(letters):

        if index == 0:
            ans.value = letter
            ans.type = __my_type__(letter)
            head = ans
        else:
            ans.previous = prev

        if index != length - 1:  # если не начало слова
            ans.next = Node(letters[index+1])
            ans.next.type = __my_type__(ans.next.value)

        if ans.type == 'v':  # гласные
            vow_n += 1
            due_to_vow_table(ans, index, letter, stress, vow_n, length)
            if ans.__dict__.__contains__('j_') and index == 0 and vow_n != stress:
                special = True

        elif ans.type == 'm':  # знаки

            if letter == 'ь':
                ans.next.soft = True
            ans.value = ''

        elif ans.type == 'c':  # согласные

            if letter == 'й':
                ans.value = 'ṷ'
            else:
                cons_tranformer(ans, letter)

        else:
            raise ValueError('Not Cyrillic')

        if ans.value == '' and index != 0:
            prev = ans.previous
        else:
            if ans.value != '':
                answer.append(ans.value)
            prev = ans

        if ans.__dict__.__contains__('j_'):
            if special:
                answer.append('ṷ')
                special = False
            else:
                answer.append('j')

        ans = ans.next

    if separate is False:
        return ''.join(answer[::-1])
    return answer[::-1]


def phrase_transformer(text, separate=True):
    """
	Функция трансформирует кириллическую строку в транскрипцию.
	Функция выдает массив всех возможных вариантов фонетического разбора.
	Если параметр separate == False, результатом будет массивы отдельных звуков. 
	
	>>> phrase_transformer('под')
	[[['п', 'о', 'т']]]
	
	>>> phrase_transformer('под сосной')
	[[['п', 'ъ', 'т'], ['с', 'а', 'с', 'н', 'о', 'ṷ']]]
	
	>>> phrase_transformer('под сосной', separate=False)
	[['път', 'сасноṷ']]
    """

    def combine(terms, accum):

        last = (len(terms) == 1)
        n = len(terms[0])

        for i in range(n):
            item = accum + [terms[0][i]]

            if last:
                combinations.append(item)
            else:
                combine(terms[1:], item)

    if not isinstance(text, str):
        raise ValueError('Wrong data type')

    words = tokenize(text)

    if stresses:
        if not isinstance(stresses, list):
            raise ValueError('Wrong data type')

        if len(words) != len(stresses):
            raise ValueError('The number of stresses must be the same as the number of words')

        if not all(isinstance(x, int) for x in stresses):
            raise ValaueError('The stress values type must be int')

    answer = []
    combinations = []
    length = len(words)

    for index, word in enumerate(words):

        stop = False
        vcd = False  # озвончение, если это фраза
        st = stressed(word, st_words)

        if word in stop_words and length > 1:

            stop = True
            if index+1 <= len(words)-1 and words[index+1][0] in data.columns and data[words[index+1][0]]['vcd'] == '+':
                vcd = True
                print(1)

        answer.append([])

        if stresses:

            if separate is False:
                answer[-1].append(''.join(transcription(word, stop=stop, vcd=vcd, stress=stresses[index])))
            else:
                answer[-1].append(transcription(word, stop=stop, vcd=vcd, stress=stresses[index]))

        else:
            for stress in stressed(word, st_words):

                if stress == 'None':
                    if separate is False:
                        answer[-1].append(''.join(transcription(word, stop=stop, vcd=vcd)))
                    else:
                        answer[-1].append(transcription(word, stop=stop, vcd=vcd))

                elif separate is False:
                    answer[-1].append(''.join(transcription(word, stop=stop, vcd=vcd, stress=stress)))
                else:
                    answer[-1].append(transcription(word, stop=stop, vcd=vcd, stress=stress))

    combine(answer, [])
    return combinations
