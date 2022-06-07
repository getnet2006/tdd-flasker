from project.app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)

    def __repr__(self):
        return '<Post %r>' % self.id