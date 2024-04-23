# Flask-Website

[Main page](https://anonymousrand.xyz)

[Blog page](https://blog.anonymousrand.xyz) (don't click this one)

Huge thanks to [Miguel Grinberg's Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) and also [Noran Saber Abdelfattah's Flask blog guide](https://medium.com/@noransaber685/building-a-flask-blog-a-step-by-step-guide-for-beginners-8bffe925cd0e), otherwise this project would've taken longer and would probably have *bad practice* scribbled all over it.

And thank you to GitHub for free image "backups" in my static folders <3

# Developer notes to compensate for possibly scuffed code

Adding new `blogpage`s:
- Update `config.py` and directory names in static paths

Adding new forms:
- Make sure that all POST forms should be Ajax using FormData and should handle the custom error(s) defined in `config.py` (ref. `app/static/js/session_util.js`, `app/admin/static/admin/js/form_submit.js`, `app/blog/static/blog/blogpage/js/comments.js`)
- Always add HTML classes `login-req-form` and `auth-true`/`auth-false` when needed

Updating HTML custom errors:
- Update `config.py`, `app/routes.py` error handlers, and `app/static/js/handle_custom_errors.js`
