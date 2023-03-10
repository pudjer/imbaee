# Generated by Django 4.1.7 on 2023-02-26 00:02

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('likes', models.IntegerField(blank=True, default=0, editable=False)),
                ('views', models.IntegerField(blank=True, default=0, editable=False)),
                ('time_create', models.TimeField(auto_now_add=True)),
                ('time_update', models.TimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True, null=True)),
                ('karma', models.IntegerField(blank=True, default=0, editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('name', models.CharField(max_length=15, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=31, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Relations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_karma', models.IntegerField(blank=True, default=0, editable=False)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='backend.branch')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.branch')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='backend.language'),
        ),
        migrations.AddField(
            model_name='branch',
            name='links',
            field=models.ManyToManyField(blank=True, through='backend.Relations', to='backend.branch'),
        ),
        migrations.AddField(
            model_name='branch',
            name='tags',
            field=models.ManyToManyField(blank=True, to='backend.tag'),
        ),
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.ManyToManyField(blank=True, related_name='user_language', to='backend.language'),
        ),
        migrations.AddField(
            model_name='user',
            name='learned_Branches',
            field=models.ManyToManyField(blank=True, editable=False, related_name='user_learned_Branches', to='backend.branch'),
        ),
        migrations.AddField(
            model_name='user',
            name='liked_Branches',
            field=models.ManyToManyField(blank=True, editable=False, related_name='user_liked_Branches', to='backend.branch'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='wanted_to_Branches',
            field=models.ManyToManyField(blank=True, related_name='user_wanted_to_learn_Branches', to='backend.branch'),
        ),
    ]
