from django.shortcuts import render, redirect
from django.urls import reverse # URL'дерди аттары боюнча алуу үчүн

# Викторинанын суроолору
# Ар бир суроо - бул сөздүк
# 'text' - суроонун тексти
# 'options' - жооп варианттарынын тизмеси
# 'correct_index' - 'options' тизмесиндеги туура жооптун индекси
QUESTIONS = [
    {
        'id': 1, # Суроонун уникалдуу идентификатору
        'text': "Кыргызстандын борбору кайсы шаар?",
        'options': ["Ош", "Бишкек", "Жалал-Абад", "Нарын"],
        'correct_index': 1,
        'explanation': "Туура жооп: Бишкек. Ал 1878-жылы Пишпек деген ат менен негизделген."
    },
    {
        'id': 2,
        'text': "Python тили кайсы жылы түзүлгөн?",
        'options': ["1989", "1991", "1995", "2000"],
        'correct_index': 1,
        'explanation': "Python 1991-жылы Гвидо ван Россум тарабынан түзүлгөн."
    },
    {
        'id': 3,
        'text': "Дүйнөдөгү эң бийик тоо кайсы?",
        'options': ["Кан-Теңири", "Жеңиш чокусу", "Эверест (Джомолунгма)", "К2 (Чогори)"],
        'correct_index': 2,
        'explanation': "Эверест (Джомолунгма) деңиз деңгээлинен 8848.86 метр бийиктикте жайгашкан."
    },
    {
        'id': 4,
        'text': "Django бул эмне?",
        'options': ["Программалоо тили", "Веб-фреймворк", "Маалымат базасы", "Тексттик редактор"],
        'correct_index': 1,
        'explanation': "Django – бул Python тилинде жазылган жогорку деңгээлдеги веб-фреймворк."
    }
    # Кааласаңыз, дагы суроолорду кошуңуз
]

def quiz_view(request, question_id=None):
    # Сессиядан упайды жана учурдагы суроонун индексин алуу
    score = request.session.get('quiz_score', 0)
    
    # Эгер question_id берилбесе (мис., /quiz/ биринчи жолу ачылса) же оюн жаңы башталса
    if question_id is None or 'current_question_index' not in request.session:
        request.session['current_question_index'] = 0
        request.session['quiz_score'] = 0
        score = 0
    
    current_question_index = request.session.get('current_question_index', 0)

    if request.method == 'POST':
        # Колдонуучунун жообун алуу
        selected_option_index = request.POST.get('option') # HTML формадан келет
        
        # Мурунку суроонун маалыматын алуу (жоопту текшерүү үчүн)
        # Колдонуучу жооп берген суроонун индексин сактап, аны текшерүү керек
        answered_question_index = int(request.POST.get('question_index_answered', current_question_index -1)) # Жөнөтүлгөн суроонун индекси
        
        if selected_option_index is not None and answered_question_index < len(QUESTIONS):
            selected_option_index = int(selected_option_index)
            correct_answer_index = QUESTIONS[answered_question_index]['correct_index']
            
            if selected_option_index == correct_answer_index:
                score += 1
                request.session['quiz_score'] = score
            
            # Кийинки суроого өтүү же оюнду бүтүрүү
            # current_question_index сакталып калган, аны өзгөртпөйбүз, себеби ал кийинки көрсөтүлө турган суроо
        
        # Кийинки суроого багыттоо (же жыйынтык барагына, эгер суроолор бүтсө)
        if current_question_index < len(QUESTIONS):
             # Кийинки суроонун ID'син алып, ошол суроого багыттоо
            next_question_id = QUESTIONS[current_question_index]['id']
            return redirect(reverse('quiz_question_page', args=[next_question_id]))
        else:
            return redirect(reverse('quiz_results_page'))


    # Учурдагы суроону көрсөтүү
    if current_question_index < len(QUESTIONS):
        # question_id боюнча туура суроону табуу (эгер URL аркылуу келсе)
        # Же болбосо current_question_index боюнча алуу
        question_data = None
        if question_id is not None:
            for q in QUESTIONS:
                if q['id'] == question_id:
                    question_data = q
                    # Учурдагы суроонун индексин сессияда жаңылоо
                    request.session['current_question_index'] = QUESTIONS.index(q) 
                    break
        
        # Эгер URL'де ID жок болсо же туура эмес ID болсо, биринчи суроону көрсөтүү (же ката)
        if question_data is None and current_question_index < len(QUESTIONS) :
             question_data = QUESTIONS[current_question_index]


        if question_data:
             # Кийинки суроонун индексин сессияга сактоо (POSTтон кийин колдонуу үчүн)
            request.session['current_question_index'] = QUESTIONS.index(question_data) + 1

            context = {
                'question': question_data,
                'question_index': QUESTIONS.index(question_data), # Шаблонго учурдагы суроонун индексин жөнөтүү
                'total_questions': len(QUESTIONS),
                'current_score': score
            }
            return render(request, 'quizapp/question_template.html', context)
        else: # Эгер суроо ID боюнча табылбаса
            # Оюнду башынан баштоо же ката билдирүү
            request.session.pop('current_question_index', None)
            request.session.pop('quiz_score', None)
            return redirect(reverse('quiz_start_page')) # Башкы бетке кайтаруу

    else:
        # Бардык суроолорго жооп берилди, жыйынтыкты көрсөтүү
        return redirect(reverse('quiz_results_page'))


def quiz_results_view(request):
    score = request.session.get('quiz_score', 0)
    total_questions = len(QUESTIONS)
    percentage = 0 # Демейки маани

    if total_questions > 0:
        percentage = (score / total_questions) * 100
    
    # Оюн бүткөндөн кийин сессияны тазалоо (милдеттүү эмес, бирок жакшы тажрыйба)
    # Эгер "Кайра ойноо" баскычы болсо, ошол жерде тазаласа да болот.
    # request.session.pop('current_question_index', None)
    # request.session.pop('quiz_score', None)

    context = {
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage, # Эсептелген пайызды контекстке кошуу
    }
    return render(request, 'quizapp/results_template.html', context)

# ... (start_quiz_view жана quiz_view функциялары өзгөрүүсүз калат) ...

def start_quiz_view(request):
    # Оюнду баштоодон мурун эски сессия маалыматтарын тазалоо
    if 'current_question_index' in request.session:
        request.session.pop('current_question_index')
    if 'quiz_score' in request.session:
        request.session.pop('quiz_score')
    
    # Биринчи суроого багыттоо
    if QUESTIONS:
        first_question_id = QUESTIONS[0]['id']
        return redirect(reverse('quiz_question_page', args=[first_question_id]))
    else:
        # Эгер суроо жок болсо, ката же билдирүү көрсөтүү
        return render(request, 'quizapp/no_questions_template.html') # Бул шаблонду да түзүү керек