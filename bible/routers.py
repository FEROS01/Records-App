class BibleRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'bible':
            return 'bible'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'bible':
            return 'bible'
        return None
