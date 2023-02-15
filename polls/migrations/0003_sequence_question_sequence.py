# Generated by Django 4.1.5 on 2023-02-15 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_remove_choice_votes_vote_question_voters'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='sequence',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='polls.sequence'),
            preserve_default=False,
        ),
    ]
