from datetime import datetime, timedelta


class Member:

    STATUS_ACTIVE = "ACTIVE"
    STATUS_EXPIRED = "EXPIRED"
    STATUS_SUSPENDED = "SUSPENDED"
    BENEFIT_MES_BONIFICADO = "MES_BONIFICADO"
    BENEFIT_NONE = "NONE"

    def __init__(self, id, name, email, phone, join_date, expiration_date, status = None, last_benefit = None, renewal_count = 0):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.join_date = join_date
        self.expiration_date = expiration_date
        self.status = status or self.STATUS_ACTIVE
        self.last_benefit = last_benefit or self.BENEFIT_NONE
        self.renewal_count = renewal_count

    @classmethod
    def create_new(cls, id, name, email, phone, join_date=None):
        now = datetime.now()
        # Si no se pasa fecha, se usa 'ahora' (comportamiento normal)
        # Si se pasa, simulamos un miembro antiguo (migración)
        actual_join_date = join_date if join_date else now
        return cls(
            id=id,
            name=name,
            email=email,
            phone=phone,
            join_date=actual_join_date,
            expiration_date=actual_join_date + timedelta(days=30),
            status=cls.STATUS_ACTIVE,
            last_benefit=cls.BENEFIT_NONE,
            renewal_count=0
        )

    def renew_membership(self):

        today = datetime.now()
        
        # Punto de partida: Si ya venció, empezamos desde hoy. 
        # Si aún es vigente, sumamos a lo que le queda (para no perder días).
        start_date = max(today, self.expiration_date)

        # renovación base: +1 mes
        new_expiration = start_date + timedelta(days=30)

        # regla de negocio: bono por antigüedad (> 12 meses desde join_date)
        months_as_member = (today - self.join_date).days / 30.44
        benefit_applied = self.BENEFIT_NONE
        bonus_days = 0

        if months_as_member > 12:
            bonus_days = 30
            new_expiration += timedelta(days=bonus_days)
            benefit_applied = self.BENEFIT_MES_BONIFICADO
        
        self.expiration_date = new_expiration
        self.status = self.STATUS_ACTIVE
        self.last_benefit = benefit_applied
        self.renewal_count += 1

        return {
            "new_expiration": new_expiration,
            "benefit_applied": benefit_applied,
            "bonus_days_added": bonus_days,
            "months_as_member": round(months_as_member, 1),
            "renewal_count": self.renewal_count,
        }