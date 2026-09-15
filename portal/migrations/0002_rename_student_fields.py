from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='student_id',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='grade',
            new_name='college_name',
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='college_name',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
