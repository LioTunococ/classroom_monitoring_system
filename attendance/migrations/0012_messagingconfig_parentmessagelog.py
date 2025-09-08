from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_notification'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessagingConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_template_absent', models.TextField(default='Attendance update for {name} ({session}) on {date}. Please contact the adviser.', help_text='Use {name}, {session}, {date} placeholders')),
                ('sms_template_late', models.TextField(default='Tardiness notice for {name} ({session}) on {date}.', help_text='Use {name}, {session}, {date} placeholders')),
            ],
            options={
                'verbose_name': 'Messaging Config',
            },
        ),
        migrations.CreateModel(
            name='ParentMessageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone', models.CharField(max_length=40)),
                ('session', models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], max_length=2)),
                ('date', models.DateField()),
                ('message', models.TextField()),
                ('success', models.BooleanField(default=False)),
                ('provider', models.CharField(default='twilio', max_length=20)),
                ('response_id', models.CharField(blank=True, max_length=64)),
                ('error', models.CharField(blank=True, max_length=255)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent_messages', to='attendance.student')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='parentmessagelog',
            index=models.Index(fields=['date', 'session'], name='idx_pml_date_sess'),
        ),
        migrations.AddIndex(
            model_name='parentmessagelog',
            index=models.Index(fields=['phone'], name='idx_pml_phone'),
        ),
    ]

