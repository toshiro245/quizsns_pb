import re


# home クイズ読み込み
def home_addquiz_format(quiz_post):
    message_tag = ''
    for quiz in quiz_post:
        message_tag += f'''
        <div class="quiz-item">
        <a href=\"/quizpost/quiz_detail/{quiz.id}\"></a>
        <p>{quiz.title}</p>
        <hr>
        '''

        quiz_problem = re.sub("\<.*?\>", "", quiz.problem)[:30]
        message_tag += f'''
        <p>{ quiz_problem }</p>
        <p class="quiz-create-info">
            { quiz.user.username }, { quiz.create_at.strftime("%Y-%m-%d") }&nbsp;&nbsp;
            <i class="fas fa-lg fa-heart like-red"></i>&nbsp;({ quiz.quizlist_set.count() })
        </p>
        </div>
        '''

    return message_tag


# detail 自分が投稿したクイズ読み込み
def detail_addmyquiz_format(quiz_post):
    message_tag = ''
    for quiz in quiz_post:
        message_tag += f'''  
        <div class="quiz-item">
        { quiz.title[:25] }<hr>
        '''
        quiz_problem = re.sub("\<.*?\>", "", quiz.problem)[:30]
        message_tag += f'''
        <p>{ quiz_problem }</p>
        <a href=\"/quizpost/quiz_detail/{quiz.id}\"></a>
        <p class="quiz-create-info">
            {quiz.user.username}, {quiz.create_at.strftime("%Y-%m-%d")}&nbsp;&nbsp;
            <i class="fas fa-lg fa-heart"></i>&nbsp;({ quiz.quizlist_set.count() })
        </p>
        </div>
        '''
    return message_tag


# detail いいねしたクイズの読み込み
def detail_addlikequiz_format(quiz_post):
    message_tag = ''
    for quiz in quiz_post:
        message_tag += f'''
        <div class="quiz-item">
        { quiz.quiz_post.title[:25] }<hr>
        '''
        quiz_problem = re.sub("\<.*?\>", "", quiz.quiz_post.problem)[:50]
        message_tag += f'''
        <p>{ quiz_problem }</p>
        <a href=\"/quizpost/quiz_detail/{quiz.quiz_post.id}\"></a>
        <p class="quiz-create-info">
            { quiz.user.username }, { quiz.quiz_post.create_at.strftime("%Y-%m-%d") }&nbsp;&nbsp;
            <i class="fas fa-lg fa-heart"></i>&nbsp;({ quiz.quiz_post.quizlist_set.count() })
        </p>
        </div>
        '''
    
    return message_tag