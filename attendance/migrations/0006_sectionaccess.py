from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_attendancesessionrecord'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('OFFICER', 'Student Officer'), ('ASSISTANT', 'Assistant')], default='OFFICER', max_length=16)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_access', to='attendance.section')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_access', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'section'], name='idx_secaccess_user_section')],
                'unique_together': {('user', 'section')},
            },
        ),
    ]

