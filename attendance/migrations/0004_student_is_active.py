from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0003_student_birthdate_optional"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]

