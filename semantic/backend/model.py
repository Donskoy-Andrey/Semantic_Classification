import re
import pandas as pd
import joblib
from natasha import (
    MorphVocab,
    Doc,
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NamesExtractor,
    DatesExtractor,
    AddrExtractor,
    NewsNERTagger
)


class SemanticModel:
    mapping = {
        "proxy": "доверенность",
        "contract": "договор",
        "act": "акт",
        "application": "заявление",
        "order": "приказ",
        "invoice": "счет",
        "bill": "приложение",
        "arrangement": "соглашение",
        "contract offer": "договор оферты",
        "statute": "устав",
        "determination": "решение",
    }

    replace_words = {
        "доверенность": re.compile(r"\bд\s*о\s*в\s*е\s*р\s*е\s*н\s*н\s*о\s*с\s*т\s*ь\b"),
        "договор": re.compile(r"\bд\s*о\s*г\s*о\s*в\s*о\s*р\b"),
        "акт": re.compile(r"\bа\s*к\s*т\b"),
        "заявление": re.compile(r"\bз\s*а\s*я\s*в\s*л\s*е\s*н\s*и\s*е\b"),
        "приказ": re.compile(r"\bп\s*р\s*и\s*к\s*а\s*з\b"),
        "счет": re.compile(r"\bс\s*ч\s*е\s*т\b"),
        "приложение": re.compile(r"\bп\s*р\s*и\s*л\s*о\s*ж\s*е\s*н\s*и\s*e\b"),
        "соглашение": re.compile(r"\bс\s*о\s*г\s*л\s*а\s*ш\s*е\s*н\s*и\s*e\b"),
        "договор оферты": re.compile(r"\bд\s*о\s*г\s*о\s*в\s*о\s*р\s*о\s*ф\s*е\s*р\s*т\s*ы\b"),
        "устав": re.compile(r"\bу\s*с\s*т\s*а\s*в\b"),
        "решение": re.compile(r"\bр\s*е\s*ш\s*е\s*н\s*и\s*е\b")
    }

    # Инициализация необходимых компонентов
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    ner_tagger = NewsNERTagger(emb)
    names_extractor = NamesExtractor(morph_vocab)
    dates_extractor = DatesExtractor(morph_vocab)
    addr_extractor = AddrExtractor(morph_vocab)

    # Подгрузка модели
    loaded_model = joblib.load('data/model.sav')

    def __init__(self, **kwargs):
        self.status_error = None

    def _remove_entities(self, text: str) -> str:
        if not isinstance(text, str):
            return self.status_error

        text = re.sub(r'[^а-яА-Яa-zA-Z\s<]', '', text)
        text = re.sub(r'\.\.+', '', text)
        text = re.sub(r'\s+', ' ', text)

        # Создание объекта Doc для обработки текста
        doc = Doc(text)

        # Анализ текста и извлечение сущностей
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)

        # Получение всех предлогов в тексте
        # prepositions = [token.text for token in doc.tokens if token.pos == 'ADP']

        for span in doc.spans:
            span.normalize(self.morph_vocab)
            span.extract_fact(self.names_extractor)
            span.extract_fact(self.dates_extractor)
            span.extract_fact(self.addr_extractor)

        # Удаление всех сущностей из текста
        for span in doc.spans:
            text = text.replace(span.text, '')

        # # Удаление всех предлогов из текста
        # for token in doc.tokens:
        #     if token.text in prepositions:
        #         text = text.replace(token.text, '')

        return text.lower()

    def _clear_text(self, text: str) -> str:
        if not isinstance(text, str):
            return self.status_error

        for key, value in self.replace_words.items():
            text = re.sub(value, key, text)

        # text = re.sub(r'[^;:\?!,\.\-а-яА-Яa-zA-Z\s<]', '', text)

        text = ' '.join([word for word in text.split() if len(word) > 2])
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def _natasha_lemma(self, text: str) -> str:
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)

        return ' '.join([_.lemma for _ in doc.tokens])

    def _data_processing(self, text: str) -> str:
        if not isinstance(text, str):
            return self.status_error
        text = self._remove_entities(text)
        text = self._clear_text(text)
        text = self._natasha_lemma(text)
        return text

    def predict(self,
                test_df: pd.DataFrame,
                ) -> dict:
        """
        Inference

        :param test_df: columns - [['filename', 'text']]. Should be processed!

        :return: list[class_]
        """
        test_df['text'] = test_df['text'].apply(self._data_processing)

        top_words = [
            "адрес", "акт", "бальмонт", "валюта", "весь", "выдать", "год", "город", "груз", "дата", "действовать",
            "деятельность", "директор", "доверенность", "договор", "документ", "доля", "единственный", "закон",
            "зарегистрировать", "заявление", "или", "именовать", "имущественный", "код", "комиссия", "контроль", "лицо",
            "масса", "место", "мой", "наименование", "настоящий", "номер", "общество", "ограничить", "ознакомить",
            "оплата", "ответственность", "отдел", "оферта", "паспорт", "подпись", "покупатель", "право", "при",
            "приказ", "приказывать", "просить", "работа", "работник", "регистрация", "решение", "руб", "случай",
            "соглашение", "составить", "составлять", "срок", "сторона", "сумма", "товар", "требовать", "указать",
            "условие", "услуга", "устав", "уставный", "участник", "часть", "электронный"
        ]
        for top in top_words:
            test_df[top] = test_df['text'].str.findall(top).str.len()
        test_df = test_df.drop(columns=['text'])
        preds = self.loaded_model.predict(test_df[top_words]).tolist()
        filenames = test_df['filename'].values.tolist()
        preds = dict(zip(filenames, preds))
        return preds


if __name__ == '__main__':
    test_text = "Директору ООО «Кошкин дом» Денисову Олегу Викторовичу \n От оператора горячей линии Бальмонт Сергея Валерьевича \n Заявление о переводе на полную ставку\n По условиям трудового договора от 01.03.2025 г. я работаю на 0.5 ставки, по 4 часа в день. В связи с появлением большого количества рабочего времени, прошу с 01.10.2025 г. перевести меня на полную ставку.28 сентября 2025 г. Бальмонт Сергей Валерьевич  "
    sem_model = SemanticModel()
    test_df = pd.DataFrame({'text': [test_text]})
    # test_df['text'] = test_df['text'].apply(data_processing)
    sem_model.predict(test_df)
