def create_login_token(token_model, user, serializer):
    token, created = token_model.objects.get_or_create(user=user)
    if created:
        a = user

    return token
