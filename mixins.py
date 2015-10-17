from extensions import session


class ModelMixin(object):
    @classmethod
    def get_or_create(cls, **kwargs):
        instance = session.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = cls(**kwargs)
            session.add(instance)
            session.commit()
            return instance
