import word
from django.http.response import JsonResponse
from django.shortcuts import render
from .models import Check, CheckWordL, CheckWordR, ResultWord
import login.models
import user.models
import home.models
import random

# Create your views here.


def check_num(request):
    if not request.session.get('is_login', None):
        login = False
        url = '/login/'
        message = '你还未登录，请登录后再操作'
        return render(request, 'buff.html', locals())
    login = True
    username = request.session.get('user_name')
    # 如果有未完成的，提示完成
    check_li = Check.objects.filter(username=username, finish=False)
    if check_li:
        check_id = check_li[0].id
        message = 'It has unfinished Check, confirm to Check, Or cancel to create a new Check?'
        # print(message)
        return render(request, 'check/check.html', locals())
    return render(request, 'check/check.html', locals())


def check_word(request, check_id):
    login = True
    if not request.session.get('is_login', None):
        login = False
        message = '你还未登录，请登录后再操作'
        url = '/login/'
        return render(request, 'buff.html', locals())
    username = request.session.get('user_name')
    check_li = Check.objects.filter(id=check_id)
    if not check_li:
        message = 'Something error, There are no this page!'
        url = '/check/'
        return render(request, 'buff.html', locals())
    check = check_li[0]
    if check.username != username:
        message = "You don't have authority to visit the page!"
        url = '/check/'
        return render(request, 'buff.html', locals())

    if check.type == 'r':
        word_list = CheckWordR.objects.filter(check_id=check.id)
    else:
        word_list = CheckWordL.objects.filter(check_id=check.id)

    words_dict = {}
    for i in word_list:
        enword = home.models.EnWords.objects.get(word=i.word)
        words_dict[i.word] = enword.translation

    return render(request, 'check/check_word.html', locals())


def get_words(word_type):
    if word_type == "cet-4":
        words = home.models.EnWords.objects.filter(cet4=True)
    elif word_type == "cet-6":
        words = home.models.EnWords.objects.filter(cet6=True)
    elif word_type == "highschool":
        words = home.models.EnWords.objects.filter(highschool=True)
    else:
        words = home.models.EnWords.objects.filter(other_type=word_type)
    # print(len(words))
    return words


def get_random_word(all_words, num, username):
    num = int(num)
    # 找到做过题单词
    did_words = CheckWordR.objects.filter(username=username)
    # 检查是否已经做过
    did_word = list(map(lambda x: x.word, did_words))
    words = list(filter(lambda x: x.word not in did_word, all_words))
    # print(len(all_words))
    res_list = []
    # 如果已经小于对应的num了，那么就要从做过的题随机选了
    if len(words) < num:
        lass_num = num - len(words)
        res_list = list(words) + random.sample(did_words, lass_num)
    else:
        # 产生相对应数量的不重复的随机数
        res_list = random.sample(words, num)
    return list(res_list)


def get_letter_word(all_words, letter, num, username):
    num = int(num)
    letter_words = filter(lambda x: x.word.startswith(letter), all_words)
    did_words = CheckWordL.objects.filter(letter=letter, username=username)
    words = list(filter(lambda x: x.word not in did_words, letter_words))

    if len(words) >= num:
        return list(words)[:num]
    # 如果不够，那就再随机选做过的的
    lass_num = num - len(words)
    return list(words) + random.sample(did_words, lass_num)


def save_check(words: list, check_s: Check, username: str, letter: str):
    type = check_s.type
    check_id = check_s.id
    for word in words:
        if type.lower() == 'r':
            check_word = CheckWordR()
        else:
            check_word = CheckWordL()
            check_word.letter = letter

        check_word.username = username
        check_word.check_id = check_id
        check_word.word = word.word
        check_word.if_do = False
        check_word.save()
    return True

# 创建Check


def ajax_type(request):
    if not request.is_ajax():
        data = {'status': 0, 'message': 'Maybe submit again?', }
        return JsonResponse(data)
    if not request.session.get('user_name', None):
        data = {'status': 0, 'message': 'Please login!', }
        return JsonResponse(data)
    username = request.session.get('user_name')
    select_type = request.POST.get('type')[0]
    letter = request.POST.get('letter')
    num = request.POST.get('num')

    try:
        word_type = user.models.UserWord.objects.get(username=username)
    except:
        data = {
            'status': 0, 'message': 'Please select the <a href="/user/select_word"> word_type </a>first!'}
        return JsonResponse(data)
    words = get_words(word_type.word_type)
    if select_type.lower() == 'r':
        words_list = get_random_word(words, num, username)
    else:
        words_list = get_letter_word(words, letter, num, username)

    check_0 = Check()
    check_0.username = username
    check_0.type = select_type
    check_0.finish = False
    check_0.check_num = int(num)
    check_0.save()
    save_check(words_list, check_0, username, letter)

    dy = user.models.Dynamics()
    dy.add_dynamics(username, type=select_type.upper(), target_id=check_0.id,
                    doing="create a new test check of {} words.".format(num))
    return JsonResponse({'status': 1, 'url': '/check/{}'.format(check_0.id)})


def finish(request):
    return render(request, 'check/finish.html', locals())


def if_exit(did_words: list, enword):
    for i in did_words:
        if i.word == enword.word:
            return False
    return True


# 保存Test
def ajax_save(request):
    if not request.is_ajax():
        data = {'status': 0, 'messsaage': 'Request Again?'}
        return JsonResponse(data)
    answers = request.POST.getlist('answer')
    words = request.POST.getlist('words')
    print(answers, words)
    check_id = request.POST.get("check_id")
    # print(request.POST)
    check_words = CheckWordR.objects.filter(check_id = check_id)
    if not check_words:
        check_words = CheckWordL.objects.filter(check_id=check_id)

    for check_word in check_words:
        index = words.index(check_word.word)
        check_word.if_do = True
        if answers[index] == check_word.word:
            check_word.error_or_correct = True
        else:
            check_word.error_or_correct = False
        check_word.result_word = answers[index]
        check_word.save()
    
    check = Check.objects.get(id=check_id)
    check.finish = True
    check.save()

    error_num = 0
    for i in range(len(words)):
        if words[i] != answers[i]:
            error_num += 1

    correct_num = len(words) - error_num
    score = (correct_num / len(words)) * 100

    rw = ResultWord()
    rw.check_id = check_id
    rw.error_num = error_num
    rw.score = score
    rw.save()

    dy = user.models.Dynamics()
    dy.add_dynamics(check.username, type='F', target_id=check_id, doing="Finish ther {} test check of {} words.".format(check_id, check_num))
    return JsonResponse({'status': 1, 'message': 'submit success', 'url': 'check/{}/result'.format(check_id)}) 

def check_result(request, check_id):
    if not request.session.get('is_login', None):
        login = False
        message = '你还未登录，请登录后再操作'
        url = '/login/'
        return render(request, 'buff.html', locals())
    username = request.session.get('user_name')
    check_li = Check.objects.filter(id=check_id)
    if not check_li:
        message = 'Something error, There are no this page!'
        url = '/check/'
        return render(request, 'buff.html', locals())
    check = check_li[0]
    if check.username != username:
        message = "You don't have authority to visit the page!"
        url = '/check/'
        return render(request, 'buff.html', locals())

    rw = ResultWord.objects.filter(check_id=check_id)
    if not rw:
        message = "Please finish the chek!"
        url = '/check/{}'.format(check_id)
        return render(request, 'buff.html', locals())

    if check.type == 'r':
        words = CheckWordR.objects.filter(check_id=check.id)
    else:
        words = CheckWordL.objects.filter(check_id=check.id)

    trans = []
    for i in words:
        enword = home.models.EnWords.objects.get(word=i.word)
        trans.append(enword.translation)
    num = check.check_num
    range_for = range(num)
    score = rw[0].score
    return render(request, 'check/check_result.html', locals())
