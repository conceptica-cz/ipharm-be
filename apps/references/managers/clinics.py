from updates.managers import BaseUpdatableManager


class ClinicManager(BaseUpdatableManager):
    def get_hospitals(self):
        """Return only hospital clinics"""
        return self.get_queryset().filter(is_hospital=True)

    def get_ambulances(self):
        """Return only ambulance clinics"""
        return self.get_queryset().filter(is_ambulance=True)

    def get_my_hospitals(self, user):
        """Return clinics belonging to user"""
        return self.get_hospitals().filter(hospital_users=user)

    def get_my_ambulances(self, user):
        """Return ambulances belonging to user"""
        return self.get_ambulances().filter(ambulance_users=user)
