from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from user_progress.models import UserProgress
from lexemes.models import Lexeme
from questions.models import Question

def get_user_from_token(key):
    try:
        token = Token.objects.get(key=key)
        return token.user
    except Token.DoesNotExist:
        raise exceptions.AuthenticationFailed('Invalid token')

def get_user_from_auth_request(request):
    token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    user = get_user_from_token(token_key)
    return user

def check_user_finished_course(user):
    current_user_progress = UserProgress.objects.filter(user_id=user.id, level_id=user.level_id).first()
    if current_user_progress is None:
        return False
    total_lexemes = Lexeme.objects.filter(level_id=user.level_id).count()
    total_lexemes_learned = current_user_progress.words_learned.count()
    total_questions = Question.objects.filter(level_id=user.level_id).count()
    total_questions_learned = current_user_progress.topic_progresses.filter(questions_learned__isnull=False).count()
    if total_lexemes == total_lexemes_learned and total_questions == total_questions_learned:
        current_user_progress.is_finished = True
        current_user_progress.save()
        return True
    return False
