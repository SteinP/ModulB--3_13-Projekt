class Tag:
    type:"Tag"

    # принемает имя тега,
    # если имя тэга не указать то по умолчанию тэг получит пустею строку.
    # пременная is_single определяет будет ли у тэга закрыкающий или нет. По умолсчанию (is_single=False) есть закрыкающий тэг.
    #атрибуты передаются через плавающий аргуметет ** kwargs
    def __init__(self, tag="", is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.childrens = []
        self.dic_op_in_end= {}

        if kwargs is not None:
            for attr, value in kwargs.items():
                if attr == "klass":
                    attr = "class"
                if "_" in attr:
                    attr = attr.replace("_", "-")
                if type(value) is str:
                    self.attributes[attr] = value
                else:
                    self.attributes[attr] = " ".join(value)

    def ic_op_in(self):
# '''
#     Функция принимает значение объект класса. Переменная attrs объединяет атрибуты с из значениями и если attrs на пустая строка то добавляет в переди пробел.

#         далее создаются начало, середину и концовку тэга.
#             + начало: имя тега с его атрибутами если они есть
#             + середина: текст
#             + концовка: закрытие тега с его именем.

#         также от типа класса и наличия потомков формируется начало тэга

# '''
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if attrs != "":
            attrs = " " + attrs

        if HTML == type(self) or TopLevelTag == type(self) or len(self.childrens) != 0:
            self.dic_op_in_end["opening"] = "<{tag}{attrs}>\n".format(
                tag=self.tag, attrs=attrs)

        else:
            self.dic_op_in_end["opening"] ="<{tag}{attrs}>".format(tag=self.tag, attrs=attrs)

        if self.text:
            self.dic_op_in_end["internal"] = self.text
        else:
            self.dic_op_in_end["internal"] = ""

        self.dic_op_in_end["ending"] = "</{tag}>\n".format(
            tag=self.tag)

    def __str__(self):

        self.ic_op_in()
        return_str=""
        if self.is_single:
            return self.dic_op_in_end["opening"]
        else:
            for child in self.childrens:
                return_str += str(child)
            return self.dic_op_in_end["opening"]+self.dic_op_in_end["internal"] + \
                return_str+self.dic_op_in_end["ending"]


    def __iadd__(self, UpLevelTag):
        self.childrens.append(UpLevelTag)
        return self


    def __enter__(self):
        return(self)

    def __exit__(self, type, value, traceback):
        pass


class HTML(Tag):
    type: "HTML"
# * параметр output определяет вывод строки HTML на печать в консоль если ouput = "" или на в фаил например utput="test.html"
# * а также класс всегла открываюшие и закрывающий тэг. Имя тэга всегра "html"
    def __init__(self, output=None):
        Tag.__init__(self, tag="html", is_single=False)
        self.output = output

    def __exit__(self, type, value, traceback):
        if self.output is not None:
            with open(self.output, "wt", encoding="UTF-8") as fp:
                fp.write(str(self))



class TopLevelTag(Tag):
# """
# Объекты класса TopLevelTag не содержат внутреннего текста и всегда парные.
# если имя тэга не указать то по умолчанию тэг получит пустею строку
# """
    type: "TopLevelTag"

    def __init__(self, tag=""):
        Tag.__init__(self, tag, is_single=False)



if __name__ == "__main__":
    with HTML(output="test.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body
