from exercise import Text_processor

if __name__ == '__main__':
    ex1 = Text_processor('Зовут его Николаем Петровичем Кирсановым. У него в пятнадцати верстах от постоялого дворика хорошее имение в двести душ, или, как он выражается с тех пор, как размежевался с крестьянами и завел «ферму», — в две тысячи десятин земли. Отец его, боевой генерал 1812 года, полуграмотный, грубый, но не злой русский человек, всю жизнь свою тянул лямку, командовал сперва бригадой, потом дивизией и постоянно жил в провинции, где в силу своего чина играл довольно значительную роль.')
    ex1.split_to_sentences()
    print(ex1.get_sentences())
