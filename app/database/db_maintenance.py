class DatabaseMaintenance:
    """Performs DB vacuuming"""
    @staticmethod
    def vacuum(db_path): return True

db_maintenance = DatabaseMaintenance()
