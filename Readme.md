## Docker launch    
    docker-compose up -d 
#
## Endpoints
- [/api/auth/users/](http://localhost:8000/api/auth/users/) - *User signup*
- [/api/auth/jwt/create/](http://localhost:8000/api/auth/jwt/create/) - *Obtain jwt token*
- [/api/user_activity/](http://localhost:8000/api/user_activity/) - *Information about user logins and requests*
- [/api/posts/](http://localhost:8000/api/posts/) - *Posts list*
- [/api/posts/create/](http://localhost:8000/api/posts/create/) - *Create new post*
- [/api/like_post/](http://localhost:8000/api/like_post/) - *Like a post or unlike if already liked by a user*
- [/api/analytics/](http://localhost:8000/api/analytics/) - *Analytics about like amount in certain date range (params are **date_from** and **date_to**)*
## Run Bot
    bash run_bot.sh