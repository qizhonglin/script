from flask_admin.contrib.sqla import ModelView
from . import db, admin


class Card(db.Model):
    __tablename__ = 'card'
    cardid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    category = db.Column(db.Enum("Medication", "Nutrition"), nullable=False)
    wiki_title = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return u'{0}, {1}, {2}, {3}'.format(self.cardid, self.name, self.category, self.wiki_title)

    def to_json(self):
        return {
            'cardid': self.cardid,
            'name': self.name,
            'category': self.category,
            'wiki_title': self.wiki_title
        }


class CoachPlanPackage(db.Model):
    __tablename__ = 'coach_plan_package'
    packageid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(1024))
    diagnosis = db.Column(db.String(128))

    coach_plans = db.relationship('CoachPlan', backref='coach_plan_package', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return u'{0}, {1}, {2}, {3}'.format(self.packageid, self.name, self.description, self.diagnosis)

    def to_json(self):
        return {
            'packageid': self.packageid,
            'name': self.name,
            'description': self.description,
            'diagnosis': self.diagnosis
        }


class CoachPlan(db.Model):
    __tablename__ = 'coach_plan'
    planid = db.Column(db.Integer, primary_key=True)
    packageid = db.Column(db.Integer, db.ForeignKey('coach_plan_package.packageid'), nullable=False)
    start_day = db.Column(db.Integer, nullable=False)
    end_day = db.Column(db.Integer, nullable=False)
    cardid = db.Column(db.Integer, db.ForeignKey('card.cardid'), nullable=False)

    card = db.relationship('Card', backref='coach_plan', uselist=False)

    def __repr__(self):
        return u'<CoachPlan %s>' % self.planid

    def to_json(self):
        return {
            'planid': self.planid,
            'packageid': self.packageid,
            'start_day': self.start_day,
            'end_day': self.end_day,
            'cardid': self.cardid
        }

class CardView(ModelView):
    form_excluded_columns = ['coach_plan', ]

class CoachPlanPackageView(ModelView):
    form_excluded_columns = ['coach_plans', ]

class CoachPlanView(ModelView):
    form_excluded_columns = ['card', 'coach_plan_package']

admin.add_view(CardView(Card, db.session))
admin.add_view(CoachPlanPackageView(CoachPlanPackage, db.session))
admin.add_view(ModelView(CoachPlan, db.session))