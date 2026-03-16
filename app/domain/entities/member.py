from datetime import datetime, timedelta


class Member:
    def __init__(self, id, name, join_date, expiration_date):
        self.id = id
        self.name = name
        self.join_date = join_date
        self.expiration_date = expiration_date

    def renew_membership(self):

        today = datetime.now()

        # renovación base: +1 mes
        new_expiration = self.expiration_date + timedelta(days=30)

        # regla de negocio
        months_as_member = (today - self.join_date).days / 30

        if months_as_member >= 12:
            new_expiration += timedelta(days=30)

        self.expiration_date = new_expiration