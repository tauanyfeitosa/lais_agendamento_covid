from django.contrib.auth.base_user import BaseUserManager


class CandidatoManager(BaseUserManager):

    def create_user(self, cpf, password=None):
        if not cpf:
            raise ValueError("O CPF deve ser informado.")
        cpf = self.cpf
        user = self.model(cpf=cpf)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password=None):
        user = self.create_user(
            cpf,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
