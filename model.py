import re
import random
import pickle


class TextGen:
    """Модель генерирует тексты заданной длины. Для генерации используются триграммы."""

    def __init__(self):
        # В этом поле будем хранить для каждой пары слов массив из возможных следующих слов с их вероятностями
        self.model = {}

    def save(self, fname):
        pickle.dump(self.model, open(fname, 'wb'))

    def load(self, fname):
        self.model = pickle.load(open(fname, 'rb'))

    def fit(self, text):
        tokens = get_tokens(text)
        triples = get_triples(tokens)  # Получим все тройки слов

        bi, tri = {}, {}  # создадим два словаря для подсчёта вхождений пар и троек слов

        for triple in triples:
            if triple not in tri:  # Проинициализируем дефолтные значения
                tri[triple] = 0
            if (triple[0], triple[1]) not in bi:
                bi[triple[0], triple[1]] = 0

            tri[triple] += 1
            bi[triple[0], triple[1]] += 1

        for (w1, w2, w3), freq in tri.items():  # Расчитаем частоты для каждого слова
            if (w1, w2) not in self.model:
                self.model[(w1, w2)] = [(w3, freq / bi[w1, w2])]
            else:
                self.model[(w1, w2)].append((w3, freq / bi[w1, w2]))

    def generate(self, length, is_rand, seed):
        """
        Генерация текста. Задаются параметры длины строки (количество слов), seed, а также is_rand.
        Этот параметр отвечает за принцип построения предложений. Если is_rand=True,
        то из списка возможных следующих слов выбирается случайное.
        В ином случае каждое следующее слово выбирается по максимальной вероятности.
        """
        random.seed(seed)

        w1, w2 = random.choice(tuple(self.model.keys()))
        gen_str = w1 + ' ' + w2
        gen_str = gen_str[0].upper() + gen_str[1:]

        if is_rand:
            for i in range(length - 2):
                w3 = random.choice(self.model[w1, w2])[0]
                gen_str += ' ' + w3
                w1, w2 = w2, w3
        else:
            for i in range(length - 2):
                w3 = sorted(self.model[w1, w2], key=lambda x: x[1], reverse=True)[0][0]
                gen_str += ' ' + w3
                w1, w2 = w2, w3
        gen_str += '.'

        return gen_str


def get_tokens(file):
    """Возвращает последовательность слов"""

    res = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            for word in re.findall(u'[а-я]+', line.lower()):
                res.append(word)
    return res


def get_triples(tokens):
    """Возвращает триграммы"""
    if len(tokens) <= 3:
        print('Слишком короткий текст')
    else:
        w1 = tokens[0]
        w2 = tokens[1]
        for w3 in tokens[2:]:
            yield w1, w2, w3

            w1, w2 = w2, w3  # Сдвинем последовательность
