from app import app

def init():
    from app import db
    from app.model.issue.user import User
    from app.util import get_encrypt_passwd
    db.create_all()
    u = User("admin", "admin", get_encrypt_passwd("admin"))
    u.is_admin = True
    db.session.add(u)
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)