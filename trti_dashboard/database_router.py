class ReadOnlyRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return False  # Block all migrations

DATABASE_ROUTERS = ['database_router.ReadOnlyRouter']
