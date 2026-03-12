HOT_WORDS = [

"срочно",
"кто привезет",
"нужно",
"ищу",
"кто доставит",
"кто возит",
"кто может привезти"

]

SPAM_WORDS = [

"продаю",
"куплю",
"скидка",
"акция",
"реклама",
"прайс",
"каталог"

]


def classify(text):

    for word in SPAM_WORDS:

        if word in text:
            return "SPAM"

    for word in HOT_WORDS:

        if word in text:
            return "HOT"

    return "COLD"