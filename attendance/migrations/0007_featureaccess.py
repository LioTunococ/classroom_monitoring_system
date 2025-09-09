from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_sectionaccess'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(choices=[('dashboard', 'Dashboard'), ('take_attendance', 'Take Attendance'), ('view_reports', 'View Reports'), ('manage_schoolyears', 'Manage School Years'), ('enroll_students', 'Enroll Students'), ('manage_periods', 'Manage Periods'), ('assign_section', 'Assign Section'), ('manage_students', 'Manage Students'), ('view_student_history', 'View Student History'), ('manage_reports', 'Manage Reports/NSDs')], max_length=64)),
                ('allow', models.BooleanField(default=True, help_text='Allow if checked, deny if unchecked')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_access', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'feature'], name='idx_feataccess_user_feature')],
                'unique_together': {('user', 'feature')},
            },
        ),
    ]

