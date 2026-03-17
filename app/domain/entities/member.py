from datetime import datetime, timedelta


class Member:
    def __init__(self, id, name, join_date, expiration_date):
        self.id = id
        self.name = name
        self.join_date = join_date
        self.expiration_date = expiration_date

    @classmethod
    def create_new(cls, id, name, join_date=None):
        now = datetime.now()
        # Si no se pasa fecha, se usa 'ahora' (comportamiento normal)
        # Si se pasa, simulamos un miembro antiguo (migración)
        actual_join_date = join_date if join_date else now
        return cls(
            id=id,
            name=name,
            join_date=actual_join_date,
            expiration_date=actual_join_date + timedelta(days=30)
        )

    def renew_membership(self):

        today = datetime.now()

        # renovación base: +1 mes
        new_expiration = self.expiration_date + timedelta(days=30)

        # regla de negocio
        months_as_member = (today - self.join_date).days / 30

        if months_as_member >= 12:
            new_expiration += timedelta(days=30)

        self.expiration_date = new_expiration