from sqlalchemy.orm import Query


class CustomQuery(Query):
    def get_or_create(self, **kwargs):
        instance = self.filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = self._entities[0].type(**kwargs)
            self.session.add(instance)
            self.session.commit()
            return instance


class ModelMixin(object):
    query_class = CustomQuery
